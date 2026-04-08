import style from "../styles/components/userscomponent.module.css";

export default function AddUserInputBoxes() {
  const labelsAndInputType = [
    ["Full Name", "text"],
    ["Username", "text"],
    ["Email Address", "email"],
    ["Role", "text"],
    ["Password", "password"],
    ["Confirm Password", "password"],
    ["Grade", "text"],
    ["Division", "text"],
  ];

  const labelInputContainer = labelsAndInputType.map(([label, type]) => {
    return (
      <div key={label} className={style.labelInputContainer}>
        <label>{label}</label>
        <input type={type} placeholder={`${label}...`} />
      </div>
    );
  });

  return <div className={style.addUserInputs}>{labelInputContainer}</div>;
}
