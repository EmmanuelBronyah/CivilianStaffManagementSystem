import style from "../../../../styles/components/userscomponent.module.css";
import Select from "react-select";
import ReadOnlyEmployeeData from "../EmployeeCore/ReadOnlyEmployeeDataComponent";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import { useMatch } from "react-router-dom";

export default function AbsencesInputBoxes({
  loadingData,
  formData,
  setFormData,
}) {
  const isUpdatePage = useMatch(
    "/home/employees/:serviceId/absences/edit/:absencesId",
  );

  const labelsAndInputType = [
    ["Absence", "text"],
    ["Start Date", "date"],
    ["End Date", "date"],
    ["Authority", "text"],
  ];

  const labelKey = (label) => {
    switch (label) {
      case "Absence":
        return "absence";
      case "Start Date":
        return "startDate";
      case "End Date":
        return "endDate";
      case "Authority":
        return "authority";
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
