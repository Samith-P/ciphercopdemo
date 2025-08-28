import { Result } from "../lib/db.js";

export const getResults = async (req, res) => {
  const { email } = req.body; 

  if (!email) {
    return res.status(400).json({ message: "Email in request body is required" });
  }

  try {
    const resultDocs = await Result
      .find({ email })
      .sort({ submittedAt: -1 })
      .limit(10); 

    res.status(200).json(resultDocs);
  } catch (error) {
    console.error("Error fetching results:", error.message);
    res.status(500).json({ message: "Internal Server Error" });
  }
};

export default getResults;