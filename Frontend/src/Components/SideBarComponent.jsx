import style from "../styles/components/sidebarcomponent.module.css";
import dashboardIcon from "../assets/icons/dashboard.svg";
import userIcon from "../assets/icons/user.svg";
import employeeIcon from "../assets/icons/employee.svg";
import feedsIcon from "../assets/icons/activity feed.svg";
import flagsIcon from "../assets/icons/flag.svg";
import settingsIcon from "../assets/icons/settings.svg";
import logo from "../assets/icons/logo.svg";

export default function SideBar({ className }) {
  return (
    <aside className={className}>
      <div className={style.logoContainer}>
        <span>
          <img src={logo} alt="CiviBase Logo" />
        </span>
        <p>CiviBase</p>
      </div>
      <nav>
        <ul>
          <li>
            <button>
              <span>
                <img src={dashboardIcon} alt="Dashboard Icon" />
              </span>
              <p>Dashboard</p>
            </button>
          </li>
          <li>
            <button>
              <span>
                <img src={userIcon} alt="User Icon" />
              </span>
              <p>Users</p>
            </button>
          </li>
          <li>
            <button>
              <span>
                <img src={employeeIcon} alt="Employee Icon" />
              </span>
              <p>Employees</p>
            </button>
          </li>
          <li>
            <button>
              <span>
                <img src={feedsIcon} alt="Activity Feeds Icon" />
              </span>
              <p>Activity Feeds</p>
            </button>
          </li>
          <li>
            <button>
              <span>
                <img src={flagsIcon} alt="Flags Icon" />
              </span>
              <p>Flags</p>
            </button>
          </li>
          <li>
            <button>
              <span>
                <img src={settingsIcon} alt="Settings Icon" />
              </span>
              <p>Settings</p>
            </button>
          </li>
        </ul>
      </nav>
    </aside>
  );
}
