import { useEffect, useState } from "react";
import style from "../styles/components/headercomponent.module.css";
import { MdSearch, MdFilterAlt } from "react-icons/md";
import Switch from "react-switch";
import image from "../assets/images/default.png";

export default function Header({ activePage, className }) {
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
    <header className={className}>
      <div className={style.activePageContainer}>
        <p>{activePage}</p>
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
      <div className={style.lightDarkModeContainer}>
        <Switch
          onColor="#004700"
          offColor="#ccc"
          uncheckedIcon={<div style={{ paddingLeft: 4 }}>☀️</div>}
          checkedIcon={<div style={{ paddingLeft: 4 }}>🌙</div>}
        />
      </div>
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
