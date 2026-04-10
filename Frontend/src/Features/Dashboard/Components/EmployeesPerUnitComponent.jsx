import style from "../../../styles/components/dashboardcomponent.module.css";

export default function EmployeesPerUnit({ data }) {
  const keyValue = Object.entries(data)[0];
  const [unit, total] = keyValue;

  return (
    <div className={style.individualNumberUnit}>
      <div className={style.numberOfEmployeesInUnit}>
        <p>{total}</p>
      </div>
      <div className={style.unitName}>
        <p>{unit}</p>
      </div>
    </div>
  );
}
