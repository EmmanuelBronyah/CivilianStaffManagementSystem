import style from "../../../styles/components/dashboardcomponent.module.css";
import { MdBadge } from "react-icons/md";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";

export default function EmployeeInfo({
  relatedEmployeeData,
  loadingEmployees,
}) {
  const { total_number_of_employees, inactive_employees } = relatedEmployeeData;

  const variables = [
    [
      total_number_of_employees,
      "Total Employees",
      style.totalEmployeesContainer,
    ],
    [
      inactive_employees,
      "Inactive Employees",
      style.totalInactiveEmployeesContainer,
    ],
  ];

  const employeeData = variables.map(([total, text, className]) => {
    return loadingEmployees ? (
      <BaseSkeleton height={115} />
    ) : (
      <div key={text} className={className}>
        <div className={style.iconContainer}>
          <MdBadge className={style.icon} />
        </div>
        <div className={style.total}>
          <p>{total}</p>
        </div>
        <div className={style.totalEmployees}>
          <p>{text}</p>
        </div>
      </div>
    );
  });

  return employeeData;
}
