import style from "../styles/components/dashboardcomponent.module.css";

import { useTheme } from "../context/ThemeContext";
import { useEffect, useState } from "react";
import api from "../api";
import UserInfo from "./UserInfoComponent";
import EmployeesPerUnit from "./EmployeesPerUnitComponent";
import EmployeeInfo from "./EmployeeInfoComponent";

export default function Dashboard() {
  const [totalUsersPerRole, setTotalUsersPerRole] = useState(null);
  const [totalEmployees, setTotalEmployees] = useState(null);
  const [employeesPerUnit, setEmployeesPerUnit] = useState(null);
  const [loadingUsers, setLoadingUsers] = useState(true);
  const [loadingEmployees, setLoadingEmployees] = useState(true);
  const [loadingEmployeesPerUnit, setLoadingEmployeesPerUnit] = useState(true);
  const { theme } = useTheme();

  useEffect(() => {
    getTotalUsersPerRole();
    getTotalEmployees();
    getEmployeesPerUnit();
  }, []);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/dashboard/");

    socket.onmessage = (event) => {
      const dataReceived = JSON.parse(event.data);
      const type = dataReceived.type;
      const data = dataReceived.data;

      if (type === "user_update") {
        setTotalUsersPerRole(data);
      }
    };

    socket.onclose = () => {
      console.log("Websocket disconnected");
    };

    return () => socket.close();
  }, []);

  const getTotalUsersPerRole = async () => {
    try {
      const res = await api.get("/api/users/role/");

      setTotalUsersPerRole(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  const getTotalEmployees = async () => {
    try {
      const res = await api.get("/api/employees/staff/total/");

      setTotalEmployees(res.data.results);
    } catch (error) {
      console.log(error);
    }
  };

  const getEmployeesPerUnit = async () => {
    try {
      const res = await api.get("/api/employees/units/employees/");

      setEmployeesPerUnit(res.data.results);
    } catch (error) {
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
              return (
                <UserInfo
                  key={key}
                  role={key}
                  total={value}
                  loading={loadingUsers}
                />
              );
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
          <EmployeeInfo
            totalEmployees={totalEmployees}
            loadingEmployees={loadingEmployees}
          />
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
