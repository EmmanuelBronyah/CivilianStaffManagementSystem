import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { TEMP_TOKEN } from "../constants";
import Header from "../Components/HeaderComponent";
import SideBar from "../Components/SideBarComponent";
import style from "../styles/pages/dashboard.module.css";
import { useState } from "react";
import { MdAccountBox, MdBadge } from "react-icons/md";

function Dashboard() {
  const [activePage, setActivePage] = useState("Dashboard");

  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem(TEMP_TOKEN);
    localStorage.removeItem("otpTaskId");
    localStorage.removeItem("otp_expiry");
  }, []);

  const navigateToLogoutPage = () => {
    navigate("/auth/logout");
  };

  return (
    <div className={style.dashboard}>
      <SideBar
        activePage={activePage}
        setActivePage={setActivePage}
        className={style.sideBar}
      />
      <div className={style.headerMainContainer}>
        <Header activePage={activePage} className={style.header} />
        <main>
          <section>
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
                <div className={style.userInfoContainer}>
                  <div className={style.userIcon}>
                    <MdAccountBox className={style.icon} />
                  </div>
                  <div className={style.totalUsersContainer}>
                    <p>10</p>
                  </div>
                  <div className={style.userRoleContainer}>
                    <p>Administrators</p>
                  </div>
                </div>
                <div className={style.userInfoContainer}>
                  <div className={style.userIcon}>
                    <MdAccountBox className={style.icon} />
                  </div>
                  <div className={style.totalUsersContainer}>
                    <p>10</p>
                  </div>
                  <div className={style.userRoleContainer}>
                    <p>Standard Users</p>
                  </div>
                </div>
                <div className={style.userInfoContainer}>
                  <div className={style.userIcon}>
                    <MdAccountBox className={style.icon} />
                  </div>
                  <div className={style.totalUsersContainer}>
                    <p>10</p>
                  </div>
                  <div className={style.userRoleContainer}>
                    <p>Viewers</p>
                  </div>
                </div>
              </div>
            </div>
            <div className={style.genderDistribution}>
              <p>Gender Distribution</p>
            </div>
            <div className={style.pension}>
              <p>Employees Due For Pension Each Year</p>
            </div>
          </section>
          <section>
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
                    <p>5678</p>
                  </div>
                  <div className={style.totalEmployees}>
                    <p>Total Employees</p>
                  </div>
                </div>
                <div className={style.employeesPerUnit}>
                  <div>
                    <p>Employees Per Unit</p>
                  </div>
                  <div className={style.numberUnitContainer}>
                    <div>
                      <div>
                        <p>4562</p>
                      </div>
                      <div>37 MIL</div>
                    </div>
                    <div>
                      <div>
                        <p>928</p>
                      </div>
                      <div>4Bn</div>
                    </div>
                  </div>
                  <div>
                    <p>View More</p>
                  </div>
                </div>
              </div>
            </div>
            <div className={style.feedsContainer}>
              <p>Recent Activity Feeds</p>
            </div>
          </section>
        </main>
      </div>
      {/* <button onClick={navigateToLogoutPage}>Logout</button>; */}
    </div>
  );
}

export default Dashboard;
