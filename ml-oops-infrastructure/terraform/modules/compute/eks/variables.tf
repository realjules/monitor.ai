variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "cluster_version" {
  description = "Kubernetes version to use for the EKS cluster"
  type        = string
  default     = "1.24"
}

variable "vpc_id" {
  description = "VPC where the cluster and workers will be deployed"
  type        = string
}

variable "subnet_ids" {
  description = "A list of subnet IDs where the nodes/node groups will be deployed"
  type        = list(string)
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
}

variable "node_groups" {
  description = "Node groups configuration"
  type = object({
    general = object({
      desired_size    = number
      max_size        = number
      min_size        = number
      instance_types  = list(string)
    })
    gpu = object({
      desired_size    = number
      max_size        = number
      min_size        = number
      instance_types  = list(string)
    })
  })
}