import style from "../styles/components/sidebarcomponent.module.css";
import { MdBadge } from "react-icons/md";
import SidebarButtons from "./SideBarButtonsComponent";
import { useTheme } from "../context/ThemeContext";

export default function SideBar(props) {
  const { theme, setTheme } = useTheme();
  return (
    <aside className={!theme && style.dark}>
      <div className={style.logoContainer}>
        <span>
          <MdBadge className={style.logo} />
        </span>
        <p>CiviBase</p>
      </div>
      <nav>
        <ul>
          <SidebarButtons
            activePage={props.activePage}
            setActivePage={props.setActivePage}
          />
        </ul>
      </nav>
    </aside>
  );
}
