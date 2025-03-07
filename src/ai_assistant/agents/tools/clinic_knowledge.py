from smolagents.tools import Tool


class ClinicKnowledgeTool(Tool):
    """Tool that provides comprehensive information about Clínica Bella."""

    name = "clinic_knowledge"
    description = "Returns comprehensive information about Clínica Bella, including services, treatments, procedures, and policies."
    inputs = {}  # No inputs needed - just call the tool directly
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.clinic_info = """
### About Clínica Bella
- Official name: Clínica Bella - Beauty and Wellness in Porto Alegre
- Location: Rua das Flores, 1234 - Belém Novo neighborhood, Porto Alegre - RS, 91787-000
- Contact: WhatsApp number: +55 51 99948-9818 (Only provide this to users when you're unable to answer their question or process their request)
- Phone: +55 51 99948-9818
- Email: contato@clinicabella.com.br
- Website: www.clinicabella.com.br
- Instagram: @clinicabella
- Developed by: cod3.team

### About the Clinic
Clínica Bella is a space dedicated to beauty and wellness, located in the heart of Porto Alegre, RS. Our mission is to provide high-quality aesthetic treatments with specialized professionals and state-of-the-art equipment. Our environment has been carefully designed to offer comfort and tranquility to our clients.

Our team is committed to offering high-quality care, using cutting-edge technology and certified products.

### Facility Structure
- 3 Procedure Rooms: Equipped with cutting-edge technology to ensure safety and efficacy.
- Comfortable Waiting Area: With sofas, magazines, and free Wi-Fi.
- Support Space: Bathrooms and resting area for clients.
- Private Parking: With free spots for clients.

### Treatments and Procedures
#### Facial Harmonization
- Botox (botulinum toxin): R$ 400 per area
- Lip Filling (Hyaluronic Acid): R$ 800
- Facial Harmonization (Set of procedures to balance facial proportions): Price upon consultation

#### Skin Treatments
- Deep Facial Cleansing: R$ 200
- Chemical Peeling for spots and rejuvenation: R$ 250
- Microneedling for collagen production and facial rejuvenation: R$ 300 per session
- Laser for treatment of spots: Part of specialized treatments

#### Laser Hair Removal
- Starting from R$ 150 per session
- Price varies according to the area and individual needs

#### Body Procedures
- Lymphatic Drainage: Part of specialized treatments
- Modeling Massage: Part of specialized treatments

### Clinic Differentials
- Personalized service with free evaluation
- State-of-the-art equipment
- Highly trained and certified professionals
- Sophisticated and comfortable environment
- Flexible payment plans
- Safe and sanitized environment, following all health protocols
- Personalized and humanized care

### Appointments and Operations
- Operating hours: Monday to Friday, 9am to 7pm; Saturdays, 9am to 1pm; Sundays: Closed
- Scheduling: Through WhatsApp, phone, email, or through the website
- Medical insurance: Not accepted, procedures are private but special payment conditions are available
- Payment methods: Cash, credit card (up to 12 installments), debit card, and PIX
- Cancellation and rescheduling: Please notify 24 hours in advance to avoid penalties

### How to Get There
Clínica Bella is located at Rua das Flores, 1234, in the Belém Novo neighborhood, in Porto Alegre. We offer private parking for greater convenience of our clients.

### Post-Procedure and Care
- Care after facial procedures: Avoid sun exposure, massages in the area, and intense physical effort in the first 24 hours
- Chemical peeling effects: Normal for skin to peel in the days following the procedure, part of the cell renewal process
"""

    def forward(self):
        """
        Returns the comprehensive clinic information.

        Returns:
            A string containing the comprehensive information about Clínica Bella
        """
        # Return the full clinic information
        return self.clinic_info
