function onlyAdminCanEdit(role) {
  switch (role) {
    case "ADMINISTRATOR":
      return false;
    case "STANDARD USER":
      return true;
    case "VIEWER":
      return true;
  }
}

function adminAndStandardUserCanEdit(role) {
  switch (role) {
    case "ADMINISTRATOR":
      return false;
    case "STANDARD USER":
      return false;
    case "VIEWER":
      return true;
  }
}

export default function isReadOnly(label, role) {
  switch (label) {
    case "Service ID":
      return onlyAdminCanEdit(role);
    case "Last Name":
      return onlyAdminCanEdit(role);
    case "Other Names":
      return onlyAdminCanEdit(role);
    case "SSNIT Number":
      return adminAndStandardUserCanEdit(role);
    case "Category":
      return onlyAdminCanEdit(role);
    case "Appointment Date":
      return adminAndStandardUserCanEdit(role);
    case "Confirmation Date":
      return adminAndStandardUserCanEdit(role);
    case "Probation":
      return onlyAdminCanEdit(role);
    case "Entry Qualification":
      return adminAndStandardUserCanEdit(role);
    case "Unit":
      return adminAndStandardUserCanEdit(role);
    case "Grade":
      return adminAndStandardUserCanEdit(role);
    case "Station":
      return onlyAdminCanEdit(role);
    case "Date of Birth":
      return onlyAdminCanEdit(role);
    case "Gender":
      return onlyAdminCanEdit(role);
    case "Hometown":
      return adminAndStandardUserCanEdit(role);
    case "Region":
      return adminAndStandardUserCanEdit(role);
    case "Nationality":
      return adminAndStandardUserCanEdit(role);
    case "Address":
      return adminAndStandardUserCanEdit(role);
    case "Email":
      return adminAndStandardUserCanEdit(role);
    case "Marital Status":
      return adminAndStandardUserCanEdit(role);
    case "Religion":
      return adminAndStandardUserCanEdit(role);
    case "Structure":
      return adminAndStandardUserCanEdit(role);
    case "Blood Group":
      return adminAndStandardUserCanEdit(role);
    case "Disable":
      return adminAndStandardUserCanEdit(role);
    default:
      return onlyAdminCanEdit(role);
  }
}
