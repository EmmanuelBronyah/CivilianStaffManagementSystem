import style from "../styles/components/dashboardcomponent.module.css";
import { MdBadge, MdShield, MdPreview, MdPerson } from "react-icons/md";
import { useTheme } from "../context/ThemeContext";
import { useEffect, useState } from "react";
import api from "../api";
import UserInfo from "./UserInfoComponent";
import EmployeesPerUnit from "./EmployeesPerUnitComponent";

export default function Dashboard() {
  const [totalUsersPerRole, setTotalUsersPerRole] = useState(null);
  const [totalEmployees, setTotalEmployees] = useState(null);
  const [employeesPerUnit, setEmployeesPerUnit] = useState(null);
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();

  useEffect(() => {
    getTotalUsersPerRole();
    getTotalEmployees();
    getEmployeesPerUnit();
  }, []);

  const getTotalUsersPerRole = async () => {
    setLoading(true);

    try {
      const res = await api.get("/api/users/role/");
      setLoading(false);

      setTotalUsersPerRole(res.data);
    } catch (error) {
      setLoading(false);
      console.log(error);
    }
  };

  const getTotalEmployees = async () => {
    setLoading(true);

    try {
      const res = await api.get("/api/employees/staff/total/");
      setLoading(false);

      setTotalEmployees(res.data.results);
    } catch (error) {
      setLoading(false);
      console.log(error);
    }
  };

  const getEmployeesPerUnit = async () => {
    setLoading(true);

    try {
      const res = await api.get("/api/employees/units/employees/");
      setLoading(false);

      setEmployeesPerUnit(res.data.results);
    } catch (error) {
      setLoading(false);
      console.log(error);
    }
  };

  return (
    <main className={!theme && style.dark}>
      <div className={style.users}>
        <div className={style.topUserSection}>
          <div>
            <p>Users</p>
          </div>
          <div>
            <button>Add User</button>
          </div>
        </div>
        <div className={style.bottomUserSection}>
          {totalUsersPerRole &&
            Object.entries(totalUsersPerRole).map(([key, value]) => {
              return <UserInfo key={key} role={key} total={value} />;
            })}
        </div>
      </div>
      <div className={style.genderDistribution}>
        <p>Gender Distribution</p>
      </div>
      <div className={style.pension}>
        <p>Employees Due For Pension Each Year</p>
      </div>
      <div className={style.employees}>
        <div className={style.employeeTextAndButtonsSection}>
          <div>
            <p>Employee</p>
          </div>
          <div className={style.buttonContainer}>
            <button>Add Employee</button>
            <button>Generate Report</button>
          </div>
        </div>
        <div className={style.employeeUnitSection}>
          <div className={style.totalEmployeesContainer}>
            <div>
              <MdBadge className={style.icon} />
            </div>
            <div className={style.total}>
              <p>{totalEmployees}</p>
            </div>
            <div className={style.totalEmployees}>
              <p>Total Employees</p>
            </div>
          </div>
          <div className={style.employeesPerUnit}>
            <div className={style.employeePerUnitTitle}>
              <p>Employees Per Unit</p>
            </div>
            <div className={style.numberUnitContainer}>
              {employeesPerUnit &&
                employeesPerUnit.map((data) => {
                  const unitTotal = Object.entries(data)[0];
                  const [unit] = unitTotal;
                  return <EmployeesPerUnit key={unit} data={data} />;
                })}
            </div>
            <div className={style.viewMoreContainer}>
              <button>View More</button>
            </div>
          </div>
        </div>
      </div>
      <div className={style.feedsContainer}>
        <p>Recent Activity Feeds</p>
      </div>
    </main>
  );
}
