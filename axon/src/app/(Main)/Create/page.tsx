'use client'
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { config } from "@/config";
import { useState } from "react";




export default function Page() {
    const [file, setFile] = useState<File | null>(null)
    const createCourse = () => {
        const fd = new FormData()
        if (file === null) {
            return ""
        }
        fd.append("file", file)
        fetch(`${config.server}/createCourse`, {
            method: "POST",
            body: fd
        })
            .then(resp => resp.json())
            .then(d => console.log(d))
    }

    return <div className=" p-4">
        <Label>Choose A File</Label>
        <Input onChange={e => setFile(e.target.files && e.target.files[0] as File)} className="bg-neutral-200 text-black flex items-center text-center " type="file" accept=".txt" />
        <Button onClick={createCourse} className="w-full h-12 mt-4">Create Course</Button>
    </div>
}