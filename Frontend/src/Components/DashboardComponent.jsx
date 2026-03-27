import style from "../styles/components/dashboardcomponent.module.css";
import { useTheme } from "../context/ThemeContext";
import { useEffect, useState } from "react";
import api from "../api";
import UserInfo from "./UserInfoComponent";
import EmployeesPerUnit from "./EmployeesPerUnitComponent";
import EmployeeInfo from "./EmployeeInfoComponent";
import GenderChart from "./GenderChartComponent";
import RetirementChart from "./RetirementChartComponent";
import BaseSkeleton from "./SkeletonComponent";
import ActivityFeeds from "./ActivityFeedsComponent";

export default function Dashboard() {
  const [totalUsersPerRole, setTotalUsersPerRole] = useState(null);
  const [relatedEmployeeData, setRelatedEmployeeData] = useState(null);
  const [genderStat, setGenderStat] = useState(null);
  const [employeesPerUnit, setEmployeesPerUnit] = useState(null);
  const [retirementStat, setRetirementStat] = useState(null);
  const [retirementLabel, setRetirementLabel] = useState(null);
  const [feeds, setFeeds] = useState(null);
  const [loadingDashboardStat, setLoadingDashboardStat] = useState(true);

  const { theme } = useTheme();

  useEffect(() => {
    const getDashboardStat = async () => {
      try {
        const res = await api.get("/api/users/dashboard/");
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
        console.log(error.response);
      }
    };
    getDashboardStat();
  }, []);

  let socket;

  const connect = () => {
    const WS_URL = import.meta.env.VITE_WS_URL;
    socket = new WebSocket(`${WS_URL}/ws/dashboard/`);

    socket.onmessage = (event) => {
      const dataReceived = JSON.parse(event.data);
      const { type, data } = dataReceived;

      if (type === "user_update") {
        setTotalUsersPerRole(data);
      }
    };

    socket.onclose = () => {
      console.log("WebSocket disconnected. Reconnecting...");
      setTimeout(connect, 3000);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
      socket.close();
    };
  };

  useEffect(() => {
    connect();
    return () => socket && socket.close();
  }, []);

  return (
    <main className={!theme ? style.dark : ""}>
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
            {totalUsersPerRole &&
              Object.entries(totalUsersPerRole).map(([key, value]) => {
                return (
                  <UserInfo
                    key={key}
                    role={key}
                    total={value}
                    loading={loadingDashboardStat}
                  />
                );
              })}
          </div>
        </div>
        <div className={style.employees}>
          <div className={style.employeeTextAndButtonsSection}>
            <div>
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
              <BaseSkeleton height={115} width={150} />
            ) : (
              <EmployeeInfo
                relatedEmployeeData={relatedEmployeeData}
                loadingDashboardStat={loadingDashboardStat}
              />
            )}
            {loadingDashboardStat ? (
              <BaseSkeleton height={115} width={210} />
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
      <div className={style.genderPensionFeedsContainer}>
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
        <div className={style.feedsContainer}>
          {loadingDashboardStat ? (
            <BaseSkeleton width={170} height={40} />
          ) : (
            <p className={style.feedsTitle}>Recent Activity Feeds</p>
          )}
          {loadingDashboardStat ? (
            <BaseSkeleton height={"85%"} />
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
      </div>
    </main>
  );
}
