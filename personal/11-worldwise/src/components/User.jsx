import { useNavigate } from "react-router-dom";
import { useAuth } from "../Contexts/FakeAuthContext";
import styles from "./User.module.css";
function User() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
//   if (!isAuthenticated || !user) return null;
  function handleClick() {
    logout();
    navigate("/");
  }
  return (
    <div className={styles.user}>
      <img src={user.avtar} alt={user.name} />
      <span> Welcome, {user.name}</span>
      <button onClick={handleClick}>Logout</button>
    </div>
  );
}

export default User;
