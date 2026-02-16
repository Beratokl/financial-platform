output "eks_cluster_endpoint" {
  value = aws_eks_cluster.main.endpoint
}

output "rds_endpoint" {
  value = aws_db_instance.main.endpoint
}

output "vpc_id" {
  value = aws_vpc.main.id
}
