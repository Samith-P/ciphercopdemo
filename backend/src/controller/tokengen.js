import jwt from "jsonwebtoken";
import { User } from "../lib/db.js";

export const protectRoute = async (req, res, next) => {
    try {
        const token = req.cookies.jwt;
        console.log('Cookiesss:', req.cookies);
        if (!token) {
            return res.status(401).json({ message: "Unauthorized - No token provided" });
        }

        const decoded = jwt.verify(token, "mysecretkey");
        if (!decoded) {
            return res.status(402).json({ message: "Unauthorized - Invalid token" });
        }

        const user = await User.findById(decoded.userId).select("-password");
        if (!user) {
            return res.status(404).json({ message: "User not found" });
        }

        req.user = user;
        next(); 
    } catch (error) {
        console.error("Error in protectRoute middleware:", error.message);
        res.status(500).json({ message: "Internal Server Error" });
    }
};

export const generateToken=(userId,res) =>{
    const token = jwt.sign({userId},"mysecretkey",{
        expiresIn:"7d"
    })
    res.cookie("jwt",token,{
        maxAge: 60*60*1000,
        httpOnly: true,
        sameSite:"lax", 
        secure: false
    })
    return token;
};
