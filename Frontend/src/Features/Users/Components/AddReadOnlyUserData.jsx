import style from "../../../styles/components/userscomponent.module.css";

export default function ReadOnlyUserData({ initialData }) {
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
        <label>{label}</label>
        <input type="text" value={field} readOnly={true} />
      </div>
    );
  });
  return fields;
}
