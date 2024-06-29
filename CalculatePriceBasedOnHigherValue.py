class CalculatePriceBasedOnHigherValue:

    @staticmethod
    def calculate_final_price(new_value):
        """Calculate the final price based on the provided logic."""
        # Increase the price by 20%
        final_price = new_value * 1.2

        # Round the price based on the described conditions
        if final_price < 5:
            final_price = round(final_price, 1)
            if final_price % 1 in [0.1, 0.2, 0.3]:
                final_price = int(final_price) + 0.5
            elif final_price % 1 in [0.6, 0.7, 0.8, 0.9]:
                final_price = int(final_price) + 1

        elif 5 <= final_price < 10:
            final_price = int(final_price)

        elif final_price >= 10:
            remainder = final_price % 1
            if remainder in [0.1, 0.2]:
                final_price = int(final_price)
            elif remainder in [0.3, 0.4]:
                final_price = int(final_price) + 0.5
            elif remainder in [0.6, 0.7]:
                final_price = int(final_price) + 0.5
            elif remainder in [0.8, 0.9]:
                final_price = int(final_price) + 1

        return final_price