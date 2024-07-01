from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Sample customer data
customer_data = """
id,name,age,city
1,John Doe,35,New York
2,Jane Smith,42,Los Angeles
3,Michael Johnson,28,Chicago
4,Emily Williams,31,Houston
5,David Brown,47,Phoenix
"""

# Sample order data
order_data = """
order_id,customer_id,product,quantity,price
101,1,Product A,2,19.99
102,2,Product B,1,29.99
103,3,Product A,3,19.99
104,4,Product C,2,14.99
105,5,Product B,1,29.99
"""

with DAG(
    dag_id='customer_order_analysis',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    @task.bash
    def clean_data():
        # Clean customer data
        customer_cleaning_commands = """
            echo '{}' > cleaned_customers.csv
            cat cleaned_customers.csv | sed 's/,/;/g' > cleaned_customers.csv
            cat cleaned_customers.csv | awk 'NR > 1' > cleaned_customers.csv
        """.format(customer_data)

        # Clean order data
        order_cleaning_commands = """
            echo '{}' > cleaned_orders.csv
            cat cleaned_orders.csv | sed 's/,/;/g' > cleaned_orders.csv
            cat cleaned_orders.csv | awk 'NR > 1' > cleaned_orders.csv
        """.format(order_data)

        return customer_cleaning_commands + "\n" + order_cleaning_commands

    @task.bash
    def transform_data(cleaned_customers, cleaned_orders):
        # Transform customer data
        customer_transform_commands = """
            cat {cleaned_customers} | awk -F';' '{{printf "%s,%s,%s\\n", $1, $2, $3}}' > transformed_customers.csv
        """.format(cleaned_customers=cleaned_customers)

        # Transform order data
        order_transform_commands = """
            cat {cleaned_orders} | awk -F';' '{{printf "%s,%s,%s,%s,%s\\n", $1, $2, $3, $4, $5}}' > transformed_orders.csv
        """.format(cleaned_orders=cleaned_orders)

        return customer_transform_commands + "\n" + order_transform_commands

    @task.bash
    def analyze_data(transformed_customers, transformed_orders):
        analysis_commands = """
            # Calculate total revenue
            total_revenue=$(awk -F',' '{{sum += $5 * $4}} END {{printf "%.2f", sum}}' {transformed_orders})
            echo "Total revenue: $total_revenue"

            # Find customers with multiple orders
            customers_with_multiple_orders=$(
                awk -F',' '{{orders[$2]++}} END {{for (c in orders) if (orders[c] > 1) printf "%s,", c}}' {transformed_orders}
            )
            echo "Customers with multiple orders: $customers_with_multiple_orders"

            # Find most popular product
            popular_product=$(
                awk -F',' '{{products[$3]++}} END {{max=0; for (p in products) if (products[p] > max) {{max=products[p]; popular=p}}}} END {{print popular}}'
            {transformed_orders})
            echo "Most popular product: $popular_product"
        """.format(transformed_customers=transformed_customers, transformed_orders=transformed_orders)

        return analysis_commands

    cleaned_data = clean_data()
    transformed_data = transform_data(cleaned_data, cleaned_data)
    analysis_results = analyze_data(transformed_data, transformed_data)