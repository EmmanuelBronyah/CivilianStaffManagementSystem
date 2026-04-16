import style from "../../../styles/components/userscomponent.module.css";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";

export default function ReadOnlyUserData({ loading, initialData }) {
  const { createdAt, updatedAt, createdBy, updatedBy } = initialData;

  const data = [
    ["Created At", createdAt],
    ["Updated At", updatedAt],
    ["Created By", createdBy],
    ["Updated By", updatedBy],
  ];

  const fields = data.map(([label, field]) => {
    return (
      <div key={label} className={style.labelInputContainer}>
        {loading ? (
          <BaseSkeleton height={30} width={150} />
        ) : (
          <label>{label}</label>
        )}
        {loading ? (
          <BaseSkeleton height={40} />
        ) : (
          <input type="text" value={field} readOnly={true} />
        )}
      </div>
    );
  });
  return fields;
}
