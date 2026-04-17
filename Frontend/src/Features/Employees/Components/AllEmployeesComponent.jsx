import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import EmployeeData from "./EmployeeDataComponent";
import { useState, useEffect } from "react";
import Notification from "../../../Components/Common/NotificationComponent";

export default function AllEmployees() {
  const [visible, setVisible] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(true);

  const { theme } = useTheme();

  useEffect(() => {
    if (!response) return;

    setVisible(true);

    const timer = setTimeout(() => {
      setVisible(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, [response]);

  return (
    <>
      <div
        className={`${style.listEmployeesContainer} ${!theme ? style.dark : ""}`}
      >
        <div className={style.titleAndButtonsContainer}>
          <div className={style.employeeTitleAndTwoButtonsContainer}>
            <p className={style.employeesTitle}>Employees</p>
            <div className={style.twoButtonsContainer}>
              <button className={style.newEmployeeButton}>New Employee</button>
              <button className={style.advancedSearchButton}>
                Advanced Search
              </button>
            </div>
          </div>
          <button className={style.applyOccurrenceButton}>
            Apply Occurrence
          </button>
        </div>
        <div className={style.employeeListContainer}>
          <table>
            <thead>
              <tr>
                <th>Service Number</th>
                <th>Name</th>
                <th>Unit</th>
                <th>Grade</th>
                <th>Category</th>
                <th>Appointment Date</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <EmployeeData
                loading={loading}
                setLoading={setLoading}
                setResponse={setResponse}
              />
            </tbody>
          </table>
        </div>
      </div>
      <Notification isVisible={visible} response={response} />
    </>
  );
}
