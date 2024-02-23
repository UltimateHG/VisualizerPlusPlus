from maltego_trx.entities import PhoneNumber
# from maltego_trx.maltego import UIM_PARTIAL
from maltego_trx.transform import DiscoverableTransform
# from maltego_trx.overlays import OverlayPosition, OverlayType
from transforms import call_collection

class MinOnlyPhone(DiscoverableTransform):
    """
    Generate a network summary for a phone number
    """
 
    @classmethod
    def create_entities(cls, request, response):
        request.Slider = 10
        phone = request.Value 
        phone = phone.replace(" ", "")
        # try: 
        network_summary = cls.get_network_summary(phone)
        if network_summary:
            # represent "sent" and "received" as edges
            summary = network_summary[0]
            for sent in summary["sent"]:
                # print(sent)
                time_sent = summary["sent"][sent]
                entity = response.addEntity(PhoneNumber, sent)
                entity.setLinkLabel(time_sent)
                # entity.setLinkThickness(int(time_sent))
                           
    @staticmethod
    def get_network_summary(phone):
        # Database setup. I don't why it does not work in __init__.py :)
        """
        Get a network summary for a phone number
        """

        query = {"number": phone}
        # print(query)
        summary = list(call_collection.find(query, {"_id": 0}))
        # get max of the sent and received
        max_sent = min(summary[0]["sent"].values())
        max_received = min(summary[0]["received"].values())
        summary[0]["sent"] = {k: v for k, v in summary[0]["sent"].items() if v == max_sent}
        summary[0]["received"] = {k: v for k, v in summary[0]["received"].items() if v == max_received}
        # print(summary)
        return summary

