import style from "../styles/components/headercomponent.module.css";
import searchIcon from "../assets/icons/search.svg";
import filterIcon from "../assets/icons/filter.svg";

export default function Header({ className }) {
  return (
    <header className={className}>
      <div className={style.activePageContainer}>
        <p>Dashboard</p>
      </div>
      <div className={style.searchBoxContainer}>
        <div className={style.searchBox}>
          <input type="text" />
          <img
            className={style.searchIcon}
            src={searchIcon}
            alt="Search Icon"
          />
          <img
            className={style.filterIcon}
            src={filterIcon}
            alt="Filter Icon"
          />
        </div>
      </div>
      <div className={style.lightDarkModeContainer}>
        <p>toggle</p>
      </div>
      <div className={style.profileContainer}>
        <p>profile</p>
      </div>
    </header>
  );
}
