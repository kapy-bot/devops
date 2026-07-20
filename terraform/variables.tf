variable "project_name" {
  description = "Short name used as a prefix for all resource names"
  type        = string
  default     = "todoapp"
}

variable "location" {
  description = "Azure region to deploy into"
  type        = string
  default     = "eastus2"
}

variable "aks_node_count" {
  description = "Number of nodes in the default AKS node pool"
  type        = number
  default     = 1
}

variable "aks_vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_D2s_v7"
}
