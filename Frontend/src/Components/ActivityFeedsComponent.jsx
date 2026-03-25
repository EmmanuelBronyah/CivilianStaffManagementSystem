import style from "../styles/components/dashboardcomponent.module.css";

export default function ActivityFeeds({ creator, activity, created_at }) {
  return (
    <div className={style.feed}>
      <div className={style.activity}>
        <p>
          <span>Activity: </span>
          {activity}
        </p>
      </div>
      <div className={style.creator}>
        <p>
          <span>Creator: </span>
          {creator}
        </p>
      </div>
      <div className={style.createdAt}>
        <p>
          <span>Created At: </span>
          {created_at}
        </p>
      </div>
    </div>
  );
}
