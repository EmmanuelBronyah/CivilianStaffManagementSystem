import style from "../../../styles/components/dashboardcomponent.module.css";
import { useTheme } from "../../../Context/ThemeContext";
import { useEffect, useState, useRef } from "react";
import api from "../../../api";
import UserInfo from "./UserInfoComponent";
import EmployeesPerUnit from "./EmployeesPerUnitComponent";
import EmployeeInfo from "./EmployeeInfoComponent";
import GenderChart from "./GenderChartComponent";
import RetirementChart from "./RetirementChartComponent";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";
import ActivityFeeds from "../../Dashboard/Components/ActivityFeedsComponent";
import Notification from "../../../Components/Common/NotificationComponent";
import getResponseMessages from "../../../utils/extractResponseMessage";

export default function Dashboard() {
  const [totalUsersPerRole, setTotalUsersPerRole] = useState(null);
  const [relatedEmployeeData, setRelatedEmployeeData] = useState(null);
  const [genderStat, setGenderStat] = useState(null);
  const [employeesPerUnit, setEmployeesPerUnit] = useState(null);
  const [retirementStat, setRetirementStat] = useState(null);
  const [retirementLabel, setRetirementLabel] = useState(null);
  const [feeds, setFeeds] = useState(null);
  const [loadingDashboardStat, setLoadingDashboardStat] = useState(true);
  const [response, setResponse] = useState(null);
  const [visible, setVisible] = useState(false);
  const socketInstance = useRef(null);
  const reconnectRef = useRef(true);
  const socketTimerRef = useRef(null);
  const retriesRef = useRef(0);

  const { theme } = useTheme();

  useEffect(() => {
    const getDashboardStat = async () => {
      try {
        const res = await api.get("/api/employees/dashboard/");
        const { users_data, employees_data, retirement_data, feeds } = res.data;

        setTotalUsersPerRole(users_data.users_per_role);
        setRelatedEmployeeData(employees_data.related_data);
        setGenderStat(employees_data.total_gender);
        setEmployeesPerUnit(employees_data.employees_per_unit);
        setRetirementLabel(retirement_data.retirement_label);
        setRetirementStat(retirement_data.forecasted_retirees);
        setFeeds(feeds);

        setLoadingDashboardStat(false);
      } catch (error) {
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    getDashboardStat();
  }, []);

  useEffect(() => {
    const webSocketConnection = () => {
      const MAX_RETRIES = 5;
      const WS_URL = import.meta.env.VITE_WS_URL;

      const socket = new WebSocket(`${WS_URL}/ws/dashboard/`);
      socketInstance.current = socket;

      socket.onopen = () => {
        console.log("Websocket connected...");
        retriesRef.current = 0;
      };

      socket.onmessage = (event) => {
        let dataReceived;

        try {
          dataReceived = JSON.parse(event.data);
        } catch (err) {
          console.error("Invalid JSON:", err);
          return;
        }

        const { type, data } = dataReceived;

        switch (type) {
          case "user_update":
            setTotalUsersPerRole(data);
            break;
          case "employee_update":
            setRelatedEmployeeData(data.employees_data.related_data);
            setGenderStat(data.employees_data.total_gender);
            setEmployeesPerUnit(data.employees_data.employees_per_unit);
            setRetirementStat(data.retirement_data.forecasted_retirees);
            break;
          case "feeds_update":
            setFeeds(data);
            break;
        }
      };

      socket.onclose = () => {
        console.log("Websocket closed...");

        if (!reconnectRef.current) return;

        if (retriesRef.current >= MAX_RETRIES) {
          console.log("Max retries reached. Stopping reconnect.");
          reconnectRef.current = false;
          return;
        }

        const delay = Math.min(3000 * 2 ** retriesRef.current, 10000);
        retriesRef.current += 1;

        console.log(`Reconnect attempt ${retriesRef.current} in ${delay}ms`);

        if (socketTimerRef.current) {
          clearTimeout(socketTimerRef.current);
        }

        socketTimerRef.current = setTimeout(() => {
          webSocketConnection();
        }, delay);
      };

      socket.onerror = (error) => {
        console.log("Websocket error", error);
      };
    };

    reconnectRef.current = true;
    webSocketConnection();

    return () => {
      reconnectRef.current = false;

      if (socketInstance.current) {
        socketInstance.current.close();
      }

      if (socketTimerRef.current) {
        clearTimeout(socketTimerRef.current);
      }
    };
  }, []);

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
      <main className={`${style.dashboardMain} ${!theme ? style.dark : ""}`}>
        <div className={style.usersEmployeeContainer}>
          <div className={style.users}>
            <div className={style.topUserSection}>
              <div>
                {loadingDashboardStat ? (
                  <BaseSkeleton height={35} width={60} />
                ) : (
                  <p>Users</p>
                )}
              </div>
              <div>
                {loadingDashboardStat ? (
                  <BaseSkeleton height={38} width={130} />
                ) : (
                  <button>Add User</button>
                )}
              </div>
            </div>
            <div className={style.bottomUserSection}>
              <UserInfo
                totalUsersPerRole={totalUsersPerRole}
                loading={loadingDashboardStat}
              />
            </div>
          </div>
          <div className={style.employees}>
            <div className={style.employeeTextAndButtonsSection}>
              <div className={style.employeeTextContainer}>
                {loadingDashboardStat ? (
                  <BaseSkeleton height={35} width={90} />
                ) : (
                  <p>Employees</p>
                )}
              </div>
              <div className={style.buttonContainer}>
                {loadingDashboardStat ? (
                  <BaseSkeleton height={39} width={130} />
                ) : (
                  <button>Add Employee</button>
                )}

                {loadingDashboardStat ? (
                  <BaseSkeleton height={39} width={130} />
                ) : (
                  <button>Generate Report</button>
                )}
              </div>
            </div>
            <div className={style.employeeUnitSection}>
              {loadingDashboardStat ? (
                <BaseSkeleton height={115} />
              ) : (
                <EmployeeInfo
                  relatedEmployeeData={relatedEmployeeData}
                  loadingDashboardStat={loadingDashboardStat}
                />
              )}
              {loadingDashboardStat ? (
                <BaseSkeleton height={115} />
              ) : (
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
              )}
            </div>
          </div>
        </div>
        <div className={style.chartsContainer}>
          <div className={style.genderDistribution}>
            {loadingDashboardStat ? (
              <BaseSkeleton width={170} height={40} />
            ) : (
              <p>Gender Distribution</p>
            )}

            {loadingDashboardStat ? (
              <BaseSkeleton height={250} />
            ) : (
              <GenderChart genderStat={genderStat} />
            )}
          </div>
          <div className={style.pension}>
            {loadingDashboardStat ? (
              <BaseSkeleton width={300} height={40} />
            ) : (
              <p>{retirementLabel}</p>
            )}

            {loadingDashboardStat ? (
              <BaseSkeleton height={250} />
            ) : (
              <RetirementChart retirementStat={retirementStat} />
            )}
          </div>
        </div>
        <div className={style.feedsContainer}>
          {loadingDashboardStat ? (
            <BaseSkeleton width={170} height={35} />
          ) : (
            <p className={style.feedsTitle}>Recent Activity Feeds</p>
          )}
          {loadingDashboardStat ? (
            <BaseSkeleton height={"90%"} />
          ) : (
            <div className={style.feedWrapper}>
              {feeds &&
                feeds.map(({ id, creator, activity, created_at }) => {
                  return (
                    <ActivityFeeds
                      key={id}
                      creator={creator}
                      activity={activity}
                      created_at={created_at}
                    />
                  );
                })}
            </div>
          )}
        </div>
        {/* <div className={style.genderPensionFeedsContainer}>
        
      </div> */}
      </main>
      <Notification isVisible={visible} response={response} />
    </>
  );
}
