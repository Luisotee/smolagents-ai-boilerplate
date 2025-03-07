from smolagents.tools import Tool


class ClinicServicesTool(Tool):
    """Tool that provides detailed information about services offered at Clínica Bella."""

    name = "clinic_services"
    description = "Returns detailed information about specific treatments and procedures offered at Clínica Bella."
    inputs = {}
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.services_info = """
### Detailed Services Information

#### Facial Harmonization
- **Botox (Botulinum Toxin)**: Reduces expression lines and wrinkles by relaxing facial muscles. 
  Commonly applied to forehead, glabella (between eyebrows), and crow's feet. Results last 4-6 months.
- **Lip Filling**: Uses hyaluronic acid to enhance lip volume and contour. 
  Results last 6-12 months depending on the product used.
- **Full Facial Harmonization**: Personalized combination of procedures (Botox, fillers, etc.) 
  to enhance facial proportions and harmony. Consultation required for customized treatment plan.

#### Skin Treatments
- **Deep Facial Cleansing**: Thorough skin cleansing that includes extraction of blackheads and 
  impurities, followed by hydration. Recommended monthly for oily skin.
- **Chemical Peeling**: Application of acids to remove damaged outer layers of skin, 
  promoting cell renewal. Effective for treating spots, acne scars, and fine lines.
- **Microneedling**: Uses tiny needles to create micro-injuries that stimulate collagen production. 
  Excellent for skin rejuvenation, texture improvement, and scar reduction.
- **Laser for Spots**: Advanced laser technology targeting pigmented areas. 
  Multiple sessions may be required depending on spot intensity.

#### Laser Hair Removal
- Uses state-of-the-art diode laser technology
- Safe for all skin types
- Requires multiple sessions (6-8 on average) for optimal results
- Permanent reduction of hair growth
- Painless procedure with cooling system

#### Body Procedures
- **Lymphatic Drainage**: Gentle massage technique to stimulate lymphatic system, 
  reducing fluid retention and toxins.
- **Modeling Massage**: Deeper massage technique that helps shape body contours and 
  break down fat deposits.
- **Radiofrequency**: Non-invasive treatment that uses radiofrequency energy to tighten 
  skin and reduce fat cells.
- **Ultracavitation**: Uses ultrasonic waves to break down fat cells, 
  which are then naturally eliminated by the body.
"""

    def forward(self):
        """Returns detailed information about specific treatments."""
        return self.services_info
