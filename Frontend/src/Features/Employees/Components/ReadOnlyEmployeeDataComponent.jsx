import style from "../../../styles/components/employees.module.css";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";

export default function ReadOnlyEmployeeData({ loading, formData }) {
  const { createdAt, updatedAt, createdBy, updatedBy } = formData;

  const data = [
    ["Created At", createdAt],
    ["Updated At", updatedAt],
    ["Created By", createdBy],
    ["Updated By", updatedBy],
  ];

  const fields = data.map(([label, field]) => {
    return (
      <div key={label}>
        {loading ? (
          <BaseSkeleton height={30} width={150} />
        ) : (
          <label>{label}</label>
        )}
        {loading ? (
          <BaseSkeleton height={40} />
        ) : (
          <input
            className={style.primaryPageInputs}
            type="text"
            value={field || ""}
            readOnly={true}
          />
        )}
      </div>
    );
  });
  return fields;
}
