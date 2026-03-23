import style from "../styles/components/dashboardcomponent.module.css";
import BaseSkeleton from "./SkeletonComponent";

export default function EmployeesPerUnit({ data, loading }) {
  const keyValue = Object.entries(data)[0];
  const [unit, total] = keyValue;

  return (
    <div className={style.individualNumberUnit}>
      <div className={style.numberOfEmployeesInUnit}>
        {loading ? <BaseSkeleton width={40} height={32} /> : <p>{total}</p>}
      </div>
      <div className={style.unitName}>
        {loading ? <BaseSkeleton width={85} height={32} /> : <p>{unit}</p>}
      </div>
    </div>
  );
}
