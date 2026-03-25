import style from "../styles/components/dashboardcomponent.module.css";
import { MdBadge } from "react-icons/md";
import BaseSkeleton from "./SkeletonComponent";

export default function EmployeeInfo({ totalEmployees, loadingEmployees }) {
  return (
    <>
      {loadingEmployees ? (
        <BaseSkeleton height={115} width={150} />
      ) : (
        <div className={style.totalEmployeesContainer}>
          <div className={style.iconContainer}>
            <MdBadge className={style.icon} />
          </div>
          <div className={style.total}>
            <p>{totalEmployees}</p>
          </div>
          <div className={style.totalEmployees}>
            <p>Total Employees</p>
          </div>
        </div>
      )}
    </>
  );
}
