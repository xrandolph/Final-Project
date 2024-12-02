from datetime import date
from typing import List, Dict

# Class: Client
class Client:
    def __init__(self, client_id: int, name: str, contact_info: str):
        self.client_id = client_id
        self.name = name
        self.contact_info = contact_info
        self.campaigns: List[Campaign] = []

    def add_campaign(self, campaign: 'Campaign') -> None:
        """Adds a campaign to the client's list of campaigns."""
        self.campaigns.append(campaign)

    def get_client_info(self) -> Dict:
        """Returns client details as a dictionary."""
        return {
            "client_id": self.client_id,
            "name": self.name,
            "contact_info": self.contact_info,
            "campaigns": [campaign.get_campaign_summary() for campaign in self.campaigns]
        }

# Class: Campaign
class Campaign:
    def __init__(self, campaign_id: int, name: str, start_date: date, end_date: date, platform: str):
        self.campaign_id = campaign_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.platform = platform
        self.metrics: Dict = {}  # e.g., {"reach": 1000, "engagement": 200, "conversion": 50}

    def update_metrics(self, metrics: Dict) -> None:
        """Updates the campaign's performance metrics."""
        self.metrics.update(metrics)

    def get_campaign_summary(self) -> Dict:
        """Returns a summary of the campaign details and metrics."""
        return {
            "campaign_id": self.campaign_id,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "platform": self.platform,
            "metrics": self.metrics
        }

# Class: Analytics
class Analytics:
    def __init__(self):
        self.data: List = []

    def calculate_kpi(self, campaign: Campaign) -> Dict:
        """Calculates key performance indicators for a campaign."""
        metrics = campaign.metrics
        kpi = {
            "engagement_rate": metrics.get("engagement", 0) / metrics.get("reach", 1) * 100,
            "conversion_rate": metrics.get("conversion", 0) / metrics.get("reach", 1) * 100
        }
        return kpi

    def generate_report(self, campaign: Campaign) -> str:
        """Generates a summary report for a campaign."""
        kpi = self.calculate_kpi(campaign)
        report = (
            f"Campaign Report for '{campaign.name}':\n"
            f"Platform: {campaign.platform}\n"
            f"Duration: {campaign.start_date} to {campaign.end_date}\n"
            f"Metrics: {campaign.metrics}\n"
            f"Engagement Rate: {kpi['engagement_rate']:.2f}%\n"
            f"Conversion Rate: {kpi['conversion_rate']:.2f}%\n"
        )
        return report

# Example Usage
if __name__ == "__main__":
    # Create a client
    client = Client(client_id=1, name="HubSpot Marketing", contact_info="contact@hubspot.com")

    # Create a campaign
    campaign = Campaign(
        campaign_id=101,
        name="Social Media Blast",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
        platform="Facebook"
    )
    campaign.update_metrics({"reach": 10000, "engagement": 2000, "conversion": 500})

    # Add the campaign to the client
    client.add_campaign(campaign)

    # Analyze the campaign
    analytics = Analytics()
    report = analytics.generate_report(campaign)

    # Output the report and client info
    print(report)
    print(client.get_client_info())
