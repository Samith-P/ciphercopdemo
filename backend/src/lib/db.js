import mongoose from 'mongoose';

let con = null;

export const connectDB = async () => {
  try {
    con = await mongoose.connect("mongodb+srv://helloworld:helloworld@cluster0.fux16.mongodb.net/", {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log(`MONGO DB Connected: ${con.connection.host}`);
  } catch (error) {
    console.error("MongoDB connection error: " + error.message);
  }
};

// User Schema
const userSchema = new mongoose.Schema(
  {
    email: {
      type: String,
      required: true,
      unique: true,
    },
    fullName: {
      type: String,
      required: true,
    },
    password: {
      type: String,
      required: true,
    },
  },
  { timestamps: true }
);

const User = mongoose.model("User", userSchema);

// Result Schema (loose structure)
const resultSchema = new mongoose.Schema({}, { strict: false });
const Result = mongoose.model("Result", resultSchema, "results"); // Explicit collection name

export { User, Result };
