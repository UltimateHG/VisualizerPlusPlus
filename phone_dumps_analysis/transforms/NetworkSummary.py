from maltego_trx.entities import PhoneNumber
from maltego_trx.maltego import UIM_PARTIAL
from maltego_trx.transform import DiscoverableTransform

from transforms import call_collection

class NetworkSummary(DiscoverableTransform):
    """
    Generate a network summary for a phone number
    """

    @classmethod
    def create_entities(cls, request, response):
        phone = request.Value 
        phone = phone.replace(" ", "")
        # try: 
        network_summary = cls.get_network_summary(phone)
        if network_summary:
            # represent "sent" and "received" as edges
            summary = network_summary[0]
            for sent in summary["sent"]:
                # print(sent)
                test_entity = response.addEntity(PhoneNumber, sent)

    @staticmethod
    def get_network_summary(phone):
        # Database setup. I don't why it does not work in __init__.py :)
        """
        Get a network summary for a phone number
        """
        query = {"number": phone}
        # print(query)
        summary = list(call_collection.find(query, {"_id": 0}))
        # print(summary)
        return summary

# test in your terminal
if __name__ == "__main__":
    summary = NetworkSummary.get_network_summary("0363661308")
    summary = summary[0]
    for received in summary["received"]:
        print(received, summary["received"][received])
        # received_entity = response.addEntity(PhoneNumber, received)
        # add a link to the original phone number
    print(summary)