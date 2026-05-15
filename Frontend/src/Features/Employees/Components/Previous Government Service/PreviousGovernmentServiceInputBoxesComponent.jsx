import style from "../../../../styles/components/employees.module.css";
import Select from "react-select";
import ReadOnlyEmployeeData from "../EmployeeCore/ReadOnlyEmployeeDataComponent";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import { MdEdit, MdEditOff } from "react-icons/md";
import { useMatch } from "react-router-dom";

export default function PreviousGovernmentServiceInputBoxes(props) {
  const isEditPage = useMatch(
    "/home/employees/:serviceId/previousGovernmentService/edit/:previousGovernmentServiceId",
  );

  const labelsAndInputType = ["Institution", "Position", "Duration"];

  const labelKey = (label) => {
    switch (label) {
      case "Institution":
        return "institution";
      case "Duration":
        return "duration";
      case "Position":
        return "position";
      default:
        return label.toLowerCase();
    }
  };

  const fields = labelsAndInputType.map((label) => {
    return (
      <div key={label}>
        {props.loadingData ? (
          <BaseSkeleton height={35} width={150} />
        ) : (
          <label>{label}</label>
        )}
        <div className={style.occurrenceInputContainer}>
          {props.loadingData ? (
            <BaseSkeleton height={45} />
          ) : (
            <input
              className={style.primaryPageInputs}
              type="text"
              value={props.formData[labelKey(label)]}
              onChange={(e) => {
                props.setFormData((prev) => ({
                  ...prev,
                  [labelKey(label)]: e.target.value,
                }));
              }}
            />
          )}
        </div>
      </div>
    );
  });

  return (
    <div className={style.occurrenceInputs}>
      {fields}
      {isEditPage && (
        <ReadOnlyEmployeeData
          formData={props.formData}
          loading={props.loadingData}
        />
      )}
    </div>
  );
}
