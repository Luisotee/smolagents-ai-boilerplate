from smolagents.tools import Tool


class ClinicPricingTool(Tool):
    """Tool that provides pricing information for Clínica Bella services."""

    name = "clinic_pricing"
    description = "Returns pricing information for treatments and procedures offered at Clínica Bella."
    inputs = {}
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.pricing_info = """
### Treatment Pricing Information

#### Facial Harmonization
- Botox (botulinum toxin): R$ 400 per area
- Lip Filling (Hyaluronic Acid): R$ 800
- Facial Harmonization (Set of procedures to balance facial proportions): Price upon consultation

#### Skin Treatments
- Deep Facial Cleansing: R$ 200
- Chemical Peeling for spots and rejuvenation: R$ 250
- Microneedling for collagen production and facial rejuvenation: R$ 300 per session
- Laser for treatment of spots: Starting at R$ 280 per session

#### Laser Hair Removal
- Small areas (upper lip, chin, underarms): R$ 150 per session
- Medium areas (bikini line, arms): R$ 250 per session
- Large areas (legs, back): R$ 350 per session
- Full body package: R$ 1,200 per session

#### Body Procedures
- Lymphatic Drainage: R$ 180 per session
- Modeling Massage: R$ 200 per session
- Radiofrequency for body contouring: R$ 300 per session
- Ultracavitation for localized fat: R$ 280 per session

### Payment Methods
- Cash: 10% discount
- Credit card: Up to 12 installments
- Debit card
- PIX: 5% discount

### Special Packages
- 5-session package: 10% discount
- 10-session package: 15% discount
- Monthly maintenance plans available upon consultation
"""

    def forward(self):
        """Returns pricing information for Clínica Bella services."""
        return self.pricing_info
