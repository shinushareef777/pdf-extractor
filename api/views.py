import csv
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView
from django.db import connection
from .models import BelegNumber, Entry
from .serializers import BelegNumberSerializer, EntrySerializer, EntryDetailSerializer
import re
from rest_framework.views import APIView
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class BelegNumberList(ListCreateAPIView):
    """
        This view will take a csv file containing assigned_integer and belegnumber
        as a query param. Process the file and add data to the db
    """
    queryset = BelegNumber.objects.all()
    serializer_class = BelegNumberSerializer

    def post(self, request, *args, **kwargs):
        file_path = request.query_params.get("file_path")
        if not file_path:
            file_path = "task/lookup.csv"

        beleg_numbers = []

        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    assigned_integer = int(row["assigned_integer"])
                    beleg_number = int(row.get("belegnumber", ""))
                    is_exists = BelegNumber.objects.filter(assigned_integer=assigned_integer).exists()
                    if is_exists:
                        continue
                    beleg_numbers.append(
                        BelegNumber(
                            assigned_integer=assigned_integer,
                            beleg_number=beleg_number,
                        )
                    )
            if not beleg_numbers:
                return Response({"error": "Belegnumber for the assigned integers already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            BelegNumber.objects.bulk_create(beleg_numbers, batch_size=200)
            return Response(data={"message":"created"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EntriesList(ListCreateAPIView):
    """
        This will map the data from the mapToProducts csv file to a db. 
        This will make it easy get all the entry info 
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def post(cls, request, *args, **kwargs):
        entries = []
        product_nums = []
        pos = []

        with open("task/mapToProducts.csv", "r") as file:
            reader = csv.DictReader(file)

            pattern = r"Pos\.\s*(\d+(?:\.\d+)*)"

            for i, row in enumerate(reader):
                pos_num_match = re.findall(pattern, row["comments"])

                curr_pos = pos_num_match[0] if len(pos_num_match) else ""

                if curr_pos:
                    pos.append(i)
                    data = {}
                    data["pos_num"] = curr_pos
                    data["entry_body"] = row["comments"]
                    data["beleg_number"] = BelegNumber.objects.get(
                        beleg_number=int(row["belegnummer"])
                    )

                    entries.append(data)

                product_nums.append(row["artikelnummer"])
        idx = 0
        for i, j in zip(pos[:-1], pos[1:]):
            prod = [pro for pro in product_nums[i:j] if pro.strip()]
            entries[idx]["product_number"] = ",".join(prod) if len(prod) else ""
            idx += 1

        prod = [pro for pro in product_nums[j:] if pro.strip()]
        entries[idx]["product_number"] = ",".join(prod) if len(prod) else ""

        bulk_entry = []

        for entry in entries:
            bulk_entry.append(Entry(
                    pos_number = entry["pos_num"],
                    entry_body = entry["entry_body"],
                    beleg_number = entry["beleg_number"],
                    product_number = entry["product_number"]
                ))
        try:
            Entry.objects.bulk_create(bulk_entry, batch_size=200)
            return Response(data={"message":"created"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EntryDetail(RetrieveAPIView):
    """
        This will take a belenumber as a path parameter and create a csv with 
        assigned_integer, belegnumber, entry_number, product_number
    """
    def get_object(self):
        beleg_number = self.kwargs.get("bg")

        sql_query = """
            SELECT pos_number, product_number, beleg_number_id, assigned_integer  
            FROM api_entry ae  
            JOIN api_belegnumber ab ON ab.beleg_number = ae.beleg_number_id 
            WHERE beleg_number = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query, [beleg_number])
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()

        objects = []
        for row in results:
            objects.append(dict(zip(columns, row)))

        with open(f"{beleg_number}.csv", "a") as file:
            headers = [
                "assigned_integer",
                "belegnumber",
                "entry_number",
                "product_number",
            ]
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in objects:
                writer.writerow(
                    [
                        row["assigned_integer"],
                        row["beleg_number_id"],
                        row["pos_number"],
                        row["product_number"],
                    ]
                )

        return objects

    def get(self, request, *args, **kwargs):
        instances = self.get_object()
        if instances:
            return Response(instances)
        else:
            return Response({"detail": "Not found"}, status=404)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        # If the exception was not handled by DRF, return the original response
        return response

    custom_response_data = {
        "error": "An error occurred",
        "detail": str(exc),  # Include the error message
        "status_code": response.status_code,
    }

    # Customize the response data based on the status code
    if response.status_code == status.HTTP_404_NOT_FOUND:
        custom_response_data["detail"] = "Resource not found"

    # Return the custom response
    return Response(custom_response_data, status=response.status_code)

    def get(self, request):
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
