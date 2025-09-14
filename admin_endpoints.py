# Clean admin API endpoints
from fastapi import HTTPException
from datetime import datetime
from collections import Counter, defaultdict
import csv
import os
import json
import uuid

# Admin API Endpoints
async def upload_document_endpoint(doc, DOCS):
    try:
        # Generate new document ID
        doc_id = f"doc_{str(uuid.uuid4())[:8]}"
        
        # Create document object
        new_doc = {
            "id": doc_id,
            "title": doc.title,
            "text": doc.content,
            "tags": doc.tags,
            "category": doc.category,
            "uploaded_by": doc.uploaded_by,
            "uploaded_at": datetime.utcnow().isoformat()
        }
        
        # Add to DOCS dictionary
        DOCS[doc_id] = new_doc
        
        # Update sample_docs.json file
        docs_list = list(DOCS.values())
        with open("sample_docs.json", "w") as f:
            json.dump(docs_list, f, indent=2)
        
        return {
            "id": doc_id,
            "title": doc.title,
            "tags": doc.tags,
            "category": doc.category,
            "uploaded_by": doc.uploaded_by,
            "uploaded_at": new_doc["uploaded_at"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_admin_stats_endpoint(DOCS, EMPLOYEE_LOG):
    try:
        total_docs = len(DOCS)
        
        # Count employees and queries from employee log
        employees = set()
        total_queries = 0
        today_queries = 0
        today = datetime.utcnow().date()
        
        if os.path.exists(EMPLOYEE_LOG):
            with open(EMPLOYEE_LOG, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    employees.add(row["employee_id"])
                    total_queries += 1
                    query_date = datetime.fromisoformat(row["timestamp"]).date()
                    if query_date == today:
                        today_queries += 1
        
        return {
            "total_documents": total_docs,
            "active_employees": len(employees),
            "total_queries": total_queries,
            "today_queries": today_queries
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_documents_endpoint(DOCS):
    try:
        return [
            {
                "id": doc["id"],
                "title": doc["title"],
                "tags": doc.get("tags", []),
                "category": doc.get("category", "general"),
                "uploaded_by": doc.get("uploaded_by", "system"),
                "uploaded_at": doc.get("uploaded_at", "N/A")
            }
            for doc in DOCS.values()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_employee_stats_endpoint(EMPLOYEE_LOG):
    try:
        employee_stats = defaultdict(lambda: {"query_count": 0, "last_activity": None})
        
        if os.path.exists(EMPLOYEE_LOG):
            with open(EMPLOYEE_LOG, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    emp_id = row["employee_id"]
                    timestamp = row["timestamp"]
                    
                    employee_stats[emp_id]["query_count"] += 1
                    if not employee_stats[emp_id]["last_activity"] or timestamp > employee_stats[emp_id]["last_activity"]:
                        employee_stats[emp_id]["last_activity"] = timestamp
        
        result = []
        for emp_id, stats in employee_stats.items():
            result.append({
                "employee_id": emp_id,
                "query_count": stats["query_count"],
                "last_activity": stats["last_activity"]
            })
        
        # Sort by query count desc
        result.sort(key=lambda x: x["query_count"], reverse=True)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_query_history_endpoint(employee_id, query_type, date, EMPLOYEE_LOG):
    try:
        queries = []
        
        if os.path.exists(EMPLOYEE_LOG):
            with open(EMPLOYEE_LOG, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Apply filters
                    if employee_id and row["employee_id"] != employee_id:
                        continue
                    if query_type and row["query_type"] != query_type:
                        continue
                    if date:
                        query_date = datetime.fromisoformat(row["timestamp"]).date().isoformat()
                        if query_date != date:
                            continue
                    
                    queries.append({
                        "timestamp": row["timestamp"],
                        "query_id": row["query_id"],
                        "employee_id": row["employee_id"],
                        "query": row["query"],
                        "query_type": row["query_type"],
                        "doc_id": row["doc_id"] if row["doc_id"] else None
                    })
        
        # Sort by timestamp desc
        queries.sort(key=lambda x: x["timestamp"], reverse=True)
        return queries[:100]  # Limit to 100 most recent
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_analytics_endpoint(EMPLOYEE_LOG):
    try:
        # Initialize analytics data
        employee_query_counts = Counter()
        document_access_counts = Counter()
        query_type_counts = Counter()
        hourly_activity = Counter()
        
        if os.path.exists(EMPLOYEE_LOG):
            with open(EMPLOYEE_LOG, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    employee_query_counts[row["employee_id"]] += 1
                    if row["doc_id"]:
                        document_access_counts[row["doc_id"]] += 1
                    query_type_counts[row["query_type"]] += 1
                    
                    # Extract hour from timestamp
                    hour = datetime.fromisoformat(row["timestamp"]).hour
                    hourly_activity[hour] += 1
        
        # Calculate analytics
        total_employees = len(employee_query_counts)
        total_queries = sum(employee_query_counts.values())
        avg_queries = round(total_queries / total_employees, 1) if total_employees > 0 else 0
        
        most_active_employee = employee_query_counts.most_common(1)[0][0] if employee_query_counts else "None"
        most_popular_doc = document_access_counts.most_common(1)[0][0] if document_access_counts else "None"
        peak_hour = hourly_activity.most_common(1)[0][0] if hourly_activity else 0
        
        return {
            "avg_queries_per_employee": avg_queries,
            "most_popular_document": most_popular_doc,
            "most_active_employee": most_active_employee,
            "peak_usage_hour": peak_hour,
            "top_documents": [doc[0] for doc in document_access_counts.most_common(5)],
            "query_type_distribution": dict(query_type_counts),
            "daily_average": round(total_queries / 7, 1)  # Assuming 7 days of data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))