import style from "../../../../styles/components/userscomponent.module.css";
import Select from "react-select";
import ReadOnlyEmployeeData from "../EmployeeCore/ReadOnlyEmployeeDataComponent";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import { useMatch } from "react-router-dom";

export default function SpouseInputBoxes({
  loadingData,
  formData,
  setFormData,
}) {
  const isUpdatePage = useMatch(
    "/home/employees/:serviceId/spouse/edit/:spouseId",
  );

  const labelsAndInputType = [
    ["Spouse Name", "text"],
    ["Phone Number", "tel"],
    ["Address", "text"],
    ["Registration Number", "text"],
    ["Marriage Date", "date"],
    ["Marriage Place", "text"],
  ];

  const labelKey = (label) => {
    switch (label) {
      case "Spouse Name":
        return "spouseName";
      case "Registration Number":
        return "registrationNumber";
      case "Marriage Date":
        return "marriageDate";
      case "Address":
        return "address";
      case "Phone Number":
        return "phoneNumber";
      case "Marriage Place":
        return "marriagePlace";
      default:
        return label.toLowerCase();
    }
  };

  const fields = labelsAndInputType.map(([label, type]) => {
    return (
      <div key={label} className={style.labelInputContainer}>
        {loadingData ? (
          <BaseSkeleton height={30} width={150} />
        ) : (
          <label>{label}</label>
        )}

        {loadingData ? (
          <BaseSkeleton height={40} />
        ) : (
          <input
            type={type}
            value={formData[labelKey(label)]}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                [labelKey(label)]: e.target.value,
              }))
            }
          />
        )}
      </div>
    );
  });

  return (
    <div className={style.addUserInputs}>
      {fields}
      {isUpdatePage && (
        <ReadOnlyEmployeeData loading={loadingData} formData={formData} />
      )}
    </div>
  );
}
