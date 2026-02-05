output "alb_dns_name" {
  value       = aws_lb.alb.dns_name
  description = "DNS name of the load balancer"
}

output "alb_arn" {
  value       = aws_lb.alb.arn
  description = "ARN of the load balancer"
}

output "target_group_arn" {
  value       = aws_lb_target_group.tg.arn
  description = "ARN of the target group"
}

output "asg_name" {
  value       = aws_autoscaling_group.app.name
  description = "Name of the Auto Scaling Group"
}

output "asg_arn" {
  value       = aws_autoscaling_group.app.arn
  description = "ARN of the Auto Scaling Group"
}

output "launch_template_id" {
  value       = aws_launch_template.app.id
  description = "ID of the launch template"
}

output "launch_template_latest_version" {
  value       = aws_launch_template.app.latest_version
  description = "Latest version of the launch template"
}

output "alb_url" {
  value       = "http://${aws_lb.alb.dns_name}"
  description = "URL to access the application through the load balancer"
}

