import style from "../styles/components/dashboardcomponent.module.css";
import { MdBadge } from "react-icons/md";
import BaseSkeleton from "./SkeletonComponent";

export default function EmployeeInfo({ totalEmployees, loadingEmployees }) {
  return (
    <div className={style.totalEmployeesContainer}>
      <div>
        {loadingEmployees ? (
          <BaseSkeleton width={32} height={32} />
        ) : (
          <MdBadge className={style.icon} />
        )}
      </div>
      <div className={style.total}>
        {loadingEmployees ? (
          <BaseSkeleton width={32} height={32} />
        ) : (
          <p>{totalEmployees}</p>
        )}
      </div>
      <div className={style.totalEmployees}>
        {loadingEmployees ? (
          <BaseSkeleton width={"70%"} height={29} />
        ) : (
          <p>Total Employees</p>
        )}
      </div>
    </div>
  );
}
