const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");
//const { json } = require("stream/consumers");
//const { createConnection } = require("net");
const app = express();
const db =  mysql.createConnection({
    host:"localhost",
    user: "root",
    password:"Dibya@123",
    database:"student",
});
app.use(cors());
app.use(express.json());
app.get("/",(req, res) => {
    return res.json("From backend server");
})
app.get('/data',(req,res) => {
    //const sql
    q='select * from studentdata'
    db.query(q,(err,result)=>{
        console.log(result)
        res.send(result)
        return res.json(result)
    });
});
app.listen(8081, ()=> {
    console.log("listening")
});