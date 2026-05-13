import style from "../../../../styles/components/userscomponent.module.css";
import Select from "react-select";
import ReadOnlyEmployeeData from "../EmployeeCore/ReadOnlyEmployeeDataComponent";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import { useMatch } from "react-router-dom";

export default function CoursesInputBoxes({
  loadingData,
  formData,
  setFormData,
}) {
  const isUpdatePage = useMatch(
    "/home/employees/:serviceId/courses/edit/:courseId",
  );

  const labelsAndInputType = [
    ["Course Type", "text"],
    ["Place", "text"],
    ["From", "date"],
    ["To", "date"],
    ["Qualification", "text"],
    ["Result", "text"],
    ["Authority", "text"],
  ];

  const labelKey = (label) => {
    switch (label) {
      case "Course Type":
        return "courseType";
      case "Place":
        return "place";
      case "From":
        return "dateCommenced";
      case "To":
        return "dateEnded";
      case "Result":
        return "result";
      case "Qualification":
        return "qualification";
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
