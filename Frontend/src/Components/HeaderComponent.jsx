import { useEffect, useState } from "react";
import style from "../styles/components/headercomponent.module.css";
import { MdSearch, MdFilterAlt } from "react-icons/md";
import image from "../assets/images/default.png";
import ThemeToggle from "./ThemeToggleComponent";

export default function Header(props) {
  const [searchQuery, setSearchQuery] = useState("");
  const [hideSearchIcon, setHideSearchIcon] = useState(false);

  useEffect(() => {
    if (searchQuery) {
      setHideSearchIcon(true);
    } else {
      setHideSearchIcon(false);
    }
  }, [searchQuery]);

  return (
    <header>
      <div className={style.activePageContainer}>
        <p>{props.activePage}</p>
      </div>
      <div className={style.searchBoxContainer}>
        <div className={style.searchBox}>
          <input type="text" onChange={(e) => setSearchQuery(e.target.value)} />
          <MdSearch
            className={`${style.searchIcon} ${hideSearchIcon && style.hide}`}
          />
          <MdFilterAlt className={style.filterIcon} />
        </div>
      </div>
      <ThemeToggle className={style.switch} />
      <div className={style.profileContainer}>
        <div className={style.defaultUserImage}>
          <img
            width="40px"
            height="40px"
            src={image}
            alt="Default User Image"
          />
        </div>
        <div className={style.userNameRoleContainer}>
          <div className={style.username}>
            <p>Emmanuel</p>
          </div>
          <div className={style.role}>
            <p>Standard User</p>
          </div>
        </div>
      </div>
    </header>
  );
}
