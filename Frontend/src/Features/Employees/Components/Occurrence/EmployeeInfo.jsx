import style from "../../../../styles/components/applyoccurrencecomponent.module.css";
import { Link, useSearchParams } from "react-router-dom";

const EmployeeInfo = ({
  serviceId,
  lastName,
  otherNames,
  occurrenceLoading,
  onToggle,
  checked,
  showSelectedEmployees,
}) => {
  const [searchParams] = useSearchParams();
  const q = searchParams.get("q");
  const page = searchParams.get("page");

  return (
    <div
      className={`${showSelectedEmployees ? style.employeeInfoSelected : style.employeeInfo}`}
    >
      <div className={style.serviceIdContainer}>
        <Link
          to={`${!occurrenceLoading ? `/home/employees/${serviceId}` : `/home/employees/apply/occurrence?q=${q}&page=${page}`}`}
        >
          <p>{serviceId}</p>
        </Link>
      </div>
      <div className={style.nameContainer}>
        <Link
          to={`${!occurrenceLoading ? `/home/employees/${serviceId}` : `/home/employees/apply/occurrence?q=${q}&page=${page}`}`}
        >
          <p>
            {lastName} {otherNames}
          </p>
        </Link>
      </div>
      {!showSelectedEmployees && (
        <div className={style.checkboxContainer}>
          <input
            type="checkbox"
            disabled={occurrenceLoading}
            checked={checked}
            onChange={onToggle}
          />
        </div>
      )}
    </div>
  );
};

export default EmployeeInfo;
