#!/bin/bash

echo "Testing concurrent booking - 5 users trying to book the same seats simultaneously"
echo "=============================================================================="

# Run 5 concurrent requests for the SAME seats
for i in {1..5}; do
  (
    echo "User $i: Sending request..."
    response=$(curl -s -X POST 'http://localhost:8000/api/book/' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: Basic cHZpamF5OnBhc3N3b3JkMTIz' \
      --data '{
        "show_id": "show-1",
        "seat_ids": [
            "show-1-pvr-delhi-1-screen-1-A3",
            "show-1-pvr-delhi-1-screen-1-A4"
        ],
        "payment_mode": "UPI",
        "coupon_code": ""
      }')

    echo "User $i response: $response"
  ) &
done

# Wait for all background processes to complete
wait

echo ""
echo "Done! Only ONE user should have succeeded, others should see 'Seats not available' error"
