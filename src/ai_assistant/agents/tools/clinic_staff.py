from smolagents.tools import Tool


class ClinicStaffTool(Tool):
    """Tool that provides information about the professional staff at Clínica Bella."""

    name = "clinic_staff"
    description = (
        "Returns information about the professional team at Clínica Bella."
    )
    inputs = {}
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.staff_info = """
### Professional Team

#### Medical Team
- **Dr. Maria Silva**: Medical Director and Aesthetic Physician with 15 years of experience. 
  Specialized in facial harmonization and injectable procedures. CRM-RS 12345.
- **Dr. Roberto Santos**: Dermatologist with focus on laser procedures and skin treatments. 
  Over 10 years of experience in aesthetic dermatology. CRM-RS 23456.

#### Aesthetic Specialists
- **Ana Oliveira**: Senior Aesthetician with specialization in facial treatments and 
  chemical peels. 8 years at Clínica Bella.
- **Carolina Lima**: Aesthetician specialized in body procedures and post-treatment care. 
  Certified in lymphatic drainage and modeling massage.
- **Paulo Ribeiro**: Specialist in laser hair removal with certification in 
  advanced laser technologies.

#### Support Team
- **Juliana Costa**: Clinic Manager and Client Relations
- **Fernanda Alves**: Reception and Scheduling
- **Marcos Vieira**: Administrative Assistant

All professionals at Clínica Bella are certified in their respective areas and 
regularly participate in continuing education programs to stay updated with the 
latest techniques and technologies in aesthetic medicine.
"""

    def forward(self):
        """Returns information about the professional team."""
        return self.staff_info
