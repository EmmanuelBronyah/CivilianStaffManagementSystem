import style from "../../../../styles/components/applyoccurrencecomponent.module.css";

const EmployeeInfo = ({ serviceId, lastName, otherNames }) => {
  return (
    <div className={style.employeeInfo}>
      <div className={style.serviceIdContainer}>
        <p>{serviceId}</p>
      </div>
      <div className={style.nameContainer}>
        <p>
          {lastName} {otherNames}
        </p>
      </div>
      <div className={style.checkboxContainer}>
        <input type="checkbox" />
      </div>
    </div>
  );
};

export default EmployeeInfo;
