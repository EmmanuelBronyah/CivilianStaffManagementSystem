import style from "../../../../styles/components/applyoccurrencecomponent.module.css";
import { Link } from "react-router-dom";

const EmployeeInfo = ({
  serviceId,
  lastName,
  otherNames,
  onToggle,
  checked,
  showSelectedEmployees,
}) => {
  return (
    <div
      className={`${showSelectedEmployees ? style.employeeInfoSelected : style.employeeInfo}`}
    >
      <div className={style.serviceIdContainer}>
        <Link to={`/home/employees/${serviceId}`}>
          <p>{serviceId}</p>
        </Link>
      </div>
      <div className={style.nameContainer}>
        <Link to={`/home/employees/${serviceId}`}>
          <p>
            {lastName} {otherNames}
          </p>
        </Link>
      </div>
      {!showSelectedEmployees && (
        <div className={style.checkboxContainer}>
          <input type="checkbox" checked={checked} onChange={onToggle} />
        </div>
      )}
    </div>
  );
};

export default EmployeeInfo;
