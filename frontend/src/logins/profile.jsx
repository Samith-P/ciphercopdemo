import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const ProfilePage = () => {
  const [open, setOpen] = useState(false);
  const [nuser, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch("http://localhost:5001/checkAuth", {
          method: "GET",
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data);
          setUser(data.user.fullName);
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
      }
    };

    fetchUser();
  }, []);

  const handleLogout = async () => {
    const response = await fetch("http://localhost:5001/logout", {
      method: "POST",
      credentials: "include",
    });
    if (response.ok) {
      navigate("/Login");
    }
  };

  return (
    <div style={{ position: "relative", padding: "20px" }}>
      {nuser ? (
        <>
          <button
            onClick={() => setOpen(!open)}
            style={{
              position: "absolute",
              top: "10px",
              right: "10px",
              width: "40px",
              height: "40px",
              borderRadius: "50%",
              backgroundColor: "#007bff",
              color: "white",
              fontSize: "18px",
              fontWeight: "bold",
              border: "none",
              cursor: "pointer",
            }}
          >
            {nuser.charAt(0)}
          </button>

          {open && (
            <div
              style={{
                position: "absolute",
                top: "50px",
                right: "0",
                width: "200px",
                backgroundColor: "white",
                padding: "10px",
                borderRadius: "8px",
                boxShadow: "0px 0px 10px rgba(0,0,0,0.1)",
              }}
            >
              <h3 style={{ margin: "0 0 10px 0" }}>{nuser}</h3>
              <p style={{ margin: "0", fontSize: "14px", color: "gray" }}>
                {nuser.email}
              </p>
              <button onClick={handleLogout}>Logout</button>
              <button
                onClick={() => setOpen(false)}
                style={{
                  marginTop: "10px",
                  background: "red",
                  color: "white",
                  border: "none",
                  padding: "5px 10px",
                  borderRadius: "5px",
                  cursor: "pointer",
                }}
              >
                Close
              </button>
            </div>
          )}
        </>
      ) : (
        <p>Loading user...</p>
      )}
    </div>
  );
};

export default ProfilePage;
