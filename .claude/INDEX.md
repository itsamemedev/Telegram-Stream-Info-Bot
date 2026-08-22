# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (311)

```
 10830  GET              /                                                dashboard
 16927  GET              /api/abo/status                                  api_abo_status
 10929  GET              /api/active-recordings                           api_active_recordings
 17002  GET              /api/activity-pulse                              api_activity_pulse
 15965  GET              /api/ai-log                                      api_ai_log
 11327  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 26415  GET              /api/ai/anomalies                                api_ai_anomalies
 13061  POST             /api/ai/ask                                      api_ai_ask
 14299  POST             /api/ai/claude/save                              api_claude_save
 14279  GET              /api/ai/claude/status                            api_claude_status
 14317  POST             /api/ai/claude/test                              api_claude_test
 13327  GET              /api/ai/config                                   api_ai_config
 11499  GET              /api/ai/conversations                            api_ai_conversations_list
 11510  POST             /api/ai/conversations                            api_ai_conversations_create
 11520  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get
 11543  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete
 11550  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch
 11561  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send
 11694  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream
 12363  POST             /api/ai/diagnose                                 api_ai_diagnose
 26653  GET              /api/ai/forecast-storage                         api_ai_forecast_storage
 26687  GET              /api/ai/health-score/<username>                  api_ai_health_score
 11483  GET              /api/ai/models                                   api_ai_models
 26368  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive
 26348  POST             /api/ai/query                                    api_ai_query
 26521  GET              /api/ai/recommendations                          api_ai_recommendations
 26569  GET              /api/ai/report                                   api_ai_report
 26620  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice
 26479  GET              /api/ai/segments                                 api_ai_segments
 26323  GET              /api/ai/skills                                   api_ai_skills
 16762  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 16010  GET              /api/archive                                     api_archive
 16306  DELETE           /api/archive/<int:eid>                           api_archive_delete
 16165  POST             /api/archive/<int:eid>/rename                    api_archive_rename
 16143  POST             /api/archive/bulk-delete                         api_archive_bulk_delete
 16133  GET              /api/archive/check                               api_archive_check
 12470  GET              /api/archive/duplicates                          api_archive_duplicates
 12486  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete
 24496  POST             /api/archive/index/<int:rid>                     api_archive_index_one
 24461  GET              /api/archive/search                              api_archive_search
 24481  GET              /api/archive/status                              api_archive_status
 16198  POST             /api/archive/upload                              api_archive_upload
 24741  GET/POST         /api/audio/config                                api_audio_config
 24771  POST             /api/audio/testtone                              api_audio_testtone
 16868  GET/POST         /api/auto-archive-rules                          api_archive_rules
 16892  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 16896  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 13277  GET              /api/automation/status                           api_automation_status
 13299  POST             /api/automation/toggle                           api_automation_toggle
 15112  GET              /api/azrael/agents                               api_azrael_agents
 13180  POST             /api/azrael/ask                                  api_azrael_ask
 24977  GET/POST         /api/azrael/context                              api_azrael_context
 14739  GET              /api/azrael/core                                 api_azrael_core
 25111  POST             /api/azrael/live_pause                           api_azrael_live_pause
 25101  GET              /api/azrael/live_status                          api_azrael_live_status
 25119  POST             /api/azrael/live_test                            api_azrael_live_test
 15121  GET              /api/azrael/memories                             api_azrael_memories
 25167  POST             /api/azrael/persona                              api_azrael_persona_set
 25158  GET              /api/azrael/personas                             api_azrael_personas
 25195  GET              /api/azrael/piper_status                         api_azrael_piper_status
 24950  POST             /api/azrael/react                                api_azrael_react
 24986  GET              /api/azrael/reaction                             api_azrael_reaction
 25138  GET              /api/azrael/reactions                            api_azrael_reactions
 25188  GET              /api/azrael/transcript                           api_azrael_transcript
 25073  POST             /api/azrael/tts_test                             api_azrael_tts_test
 25048  GET              /api/azrael/voices                               api_azrael_voices
 25212  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11881  GET              /api/backoff-watch                               api_backoff_watch
 15736  POST             /api/backup/run                                  api_backup_run
 15702  GET              /api/backup/status                               api_backup_status
 15691  POST             /api/backup/system                               api_backup_system
 16834  GET              /api/bandwidth/live                              api_bandwidth_live
 16747  GET              /api/bookmarks                                   api_bookmarks_list
 12144  GET              /api/brain                                       api_brain
 12081  GET              /api/brain/alarms                                api_brain_alarms
 12066  GET              /api/brain/creator                               api_brain_creator
 12043  GET              /api/brain/graph                                 api_brain_graph
 12104  GET              /api/brain/growth                                api_brain_growth
 10426  GET              /api/brain/health                                api_brain_health
 25693  GET              /api/channel/categories                          api_channel_categories
 25699  POST             /api/channel/set                                 api_channel_set
 25509  GET              /api/channels/status                             api_channels_status
 24311  POST             /api/chat/send                                   api_chat_send
 15423  GET              /api/chat/send_status                            api_chat_send_status
 10910  GET              /api/checks                                      api_checks
 25014  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 24997  GET              /api/clips                                       api_clips
 25030  POST/DELETE      /api/clips/clear                                 api_clips_clear
 24616  GET              /api/cohost                                      api_cohost
 24628  POST             /api/cohost/config                               api_cohost_config
 17490  GET/POST         /api/collections                                 api_collections
 17525  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify
 17589  GET              /api/collections/<int:cid>/trackings             api_collection_trackings
 17930  GET              /api/community/stats                             api_community_stats
 27025  POST             /api/config/restore                              api_config_restore
 27010  GET              /api/config/snapshot                             api_config_snapshot
 17025  GET              /api/cookies/age                                 api_cookies_age
 10977  GET              /api/cookies/health                              api_cookies_health
 10984  POST             /api/cookies/update                              api_cookies_update
 26976  GET              /api/data/export                                 api_data_export
 18440  GET              /api/db/export                                   api_db_export
 18467  POST             /api/db/import                                   api_db_import
 18427  GET              /api/db/summary                                  api_db_summary
 24542  GET              /api/debug/threads                               api_debug_threads
 27911  GET              /api/defense/attacks                             api_defense_attacks
 27878  GET              /api/defense/crowdsec                            api_defense_crowdsec
 27896  GET              /api/defense/fail2ban                            api_defense_fail2ban
 27602  GET              /api/defense/overview                            api_defense_overview
 15798  POST             /api/discord/announce                            api_discord_announce
 15526  GET              /api/discord/clips_week                          api_discord_clips_week
 15742  GET              /api/discord/community                           api_discord_community
 15451  GET              /api/discord/invite                              api_discord_invite
 14870  GET              /api/discord/overview                            api_discord_overview
 14956  POST             /api/discord/webhook_test                        api_discord_webhook_test
 18007  POST             /api/donations/add                               api_donations_add
 18040  GET              /api/donations/manual                            api_donations_manual
 18048  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 17943  POST             /api/donations/reset                             api_donations_reset
 18064  GET              /api/donations/summary                           api_donations_summary
 16816  GET              /api/events                                      api_events
 15573  GET              /api/events/stream                               api_events_stream
 19095  GET              /api/evolution/changelog                         api_evolution_changelog
 19080  GET              /api/evolution/history                           api_evolution_history
 19020  GET              /api/evolution/learned                           api_evolution_learned
 19042  GET              /api/evolution/proposals                         api_evolution_proposals
 19063  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 19010  POST             /api/evolution/run                               api_evolution_run
 19110  GET              /api/evolution/snapshots                         api_evolution_snapshots
 18975  GET              /api/evolution/status                            api_evolution_status
 18274  GET              /api/finanzamt/entries                           api_finanzamt_entries
 18294  POST             /api/finanzamt/entry                             api_finanzamt_add
 18321  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 16829  GET              /api/forecast/storage                            api_forecast_storage
 13315  GET              /api/freeai/status                               api_freeai_status
 14812  GET              /api/health                                      api_health
 11799  GET              /api/health-score                                api_health_score
 16847  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 16843  GET              /api/heatmap/recordings                          api_heatmap_recordings
 24665  GET              /api/highlights                                  api_highlights
 24677  POST             /api/highlights/config                           api_highlights_config
 17400  GET              /api/insights/activity-clock                     api_insights_activity_clock
 17275  GET              /api/insights/best-times/<username>              api_insights_best_times
 17382  GET              /api/insights/catch-rate                         api_insights_catch_rate
 17357  GET              /api/insights/growth/<username>                  api_insights_growth
 17421  GET              /api/insights/leaderboard                        api_insights_leaderboard
 17308  GET              /api/insights/reliability                        api_insights_reliability
 17331  GET              /api/insights/session-stats                      api_insights_session_stats
 17455  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer
 25550  GET              /api/kick/channel                                api_kick_channel
 25571  POST             /api/kick/channel                                api_kick_channel_set
 14539  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 14607  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 14585  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 14524  GET              /api/kick/oauth/start                            api_kick_oauth_start
 14564  GET              /api/kick/oauth/status                           api_kick_oauth_status
 24789  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 24858  POST             /api/kickmod/config                              api_kickmod_config
 24903  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 24917  GET              /api/kickmod/learned                             api_kickmod_learned
 24944  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 24924  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 25255  POST             /api/kickmod/say                                 api_kickmod_say
 25231  POST             /api/kickmod/start                               api_kickmod_start
 24829  GET              /api/kickmod/status                              api_kickmod_status
 25242  POST             /api/kickmod/stop                                api_kickmod_stop
 10762  POST             /api/login                                       dashboard_login_submit
 17915  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13766  POST             /api/marketing/config                            api_marketing_config
 13791  GET              /api/marketing/preview                           api_marketing_preview
 13801  POST             /api/marketing/send-now                          api_marketing_send_now
 13740  GET              /api/marketing/status                            api_marketing_status
 13758  POST             /api/marketing/toggle                            api_marketing_toggle
 24692  GET              /api/moderation/feed                             api_moderation_feed
 14370  POST             /api/news/config                                 api_news_config
 14336  GET              /api/news/creators                               api_news_creators
 14347  POST             /api/news/creators/generate                      api_news_creators_generate
 14412  POST             /api/news/generate-now                           api_news_generate_now
 14407  GET              /api/news/items                                  api_news_items
 14398  GET              /api/news/preview                                api_news_preview
 14266  GET              /api/news/status                                 api_news_status
 14362  POST             /api/news/toggle                                 api_news_toggle
 17772  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 15344  GET              /api/notify/status                               api_notify_status
 15355  POST             /api/notify/test                                 api_notify_test
 15330  GET              /api/ops/audit                                   api_ops_audit
 17843  GET              /api/ops/db-stats                                api_ops_db_stats
 17871  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 15136  GET              /api/ops/errors                                  api_ops_errors
 17792  GET              /api/ops/healthcheck                             api_ops_healthcheck
 18522  GET              /api/ops/log-tail                                api_ops_log_tail
 13160  GET              /api/ops/logtail                                 api_ops_logtail
 15077  GET              /api/ops/metrics                                 api_ops_metrics
 15060  GET              /api/ops/resource_history                        api_ops_resource_history
 18496  GET              /api/ops/version                                 api_ops_version
 11180  GET              /api/outcomes                                    api_outcomes
 26174  POST             /api/overlay/config                              api_overlay_config
 26161  POST             /api/overlay/event                               api_overlay_event
 26066  GET              /api/overlay/state                               api_overlay_state
 11213  GET              /api/profile/<username>                          api_profile
 17033  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 16855  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 16981  GET              /api/proxy/heatmap                               api_proxy_heatmap
 16958  GET              /api/proxy/trend                                 api_proxy_trend
 14240  GET              /api/public/stats                                api_public_stats
 10864  GET              /api/pulse                                       api_pulse
 15989  GET              /api/recording-attempts                          api_recording_attempts
 24246  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 24224  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 24265  POST             /api/restream/<int:rid>/start                    api_restream_start
 24563  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 26028  GET              /api/restream/chatfeed                           api_restream_chatfeed
 24200  POST             /api/restream/create                             api_restream_create
 14615  GET              /api/restream/deck                               api_restream_deck
 13251  GET              /api/restream/health                             api_restream_health
 26050  POST             /api/restream/layout                             api_restream_layout
 24173  GET              /api/restream/list                               api_restream_list
 13224  POST             /api/restream/report                             api_restream_report
 24576  POST             /api/restream/start_all                          api_restream_start_all
 24602  POST             /api/restream/stop_all                           api_restream_stop_all
 13514  GET              /api/restream/testpush                           api_testpush_status
 13539  POST             /api/restream/testpush                           api_testpush_run
 18180  GET              /api/restream/verify                             api_restream_verify
 15504  GET              /api/retention/preview                           api_retention_preview
 15513  POST             /api/retention/run                               api_retention_run
 27091  POST             /api/schedule/add                                api_schedule_add
 27081  GET              /api/schedule/list                               api_schedule_list
 27116  POST             /api/schedule/remove                             api_schedule_remove
 15386  POST             /api/scheduler/add                               api_scheduler_add
 15407  POST             /api/scheduler/delete                            api_scheduler_delete
 15373  GET              /api/scheduler/list                              api_scheduler_list
 15461  POST             /api/scheduler/toggle                            api_scheduler_toggle
 16732  GET              /api/search                                      api_search
 27649  GET              /api/selftest                                    api_selftest
 24282  GET              /api/shield/stats                                api_shield_stats
 10883  GET              /api/stats                                       api_stats
 16996  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 16923  GET              /api/stats/tiktok-status                         api_tiktok_status
 27056  GET              /api/stats/timeline                              api_stats_timeline
 10951  GET              /api/storage                                     api_storage
 10958  POST             /api/storage/cleanup                             api_storage_cleanup
 16909  GET              /api/stream/inspect/<username>                   api_stream_inspect
 13201  GET              /api/stream/timeline                             api_stream_timeline
 14944  GET              /api/stream/transcript                           api_stream_transcript
 26724  GET              /api/streamer/compare                            api_streamer_compare
 26923  POST             /api/streamer/delete/<username>                  api_streamer_delete
 15478  GET              /api/streamer/detail                             api_streamer_detail
 26948  GET              /api/streamer/digest/<username>                  api_streamer_digest
 26828  GET              /api/streamer/dormant                            api_streamer_dormant
 26904  GET              /api/streamer/exists/<username>                  api_streamer_exists
 26783  GET              /api/streamer/journal/<username>                 api_streamer_journal
 26748  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 26808  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14779  GET              /api/streamers/wall                              api_streamers_wall
 11100  GET              /api/summary/preview                             api_summary_preview
 16418  GET              /api/system                                      api_system
 16314  GET              /api/system-resources                            api_system_resources
 18128  GET              /api/system/check_timing                         api_check_timing
 18408  GET              /api/system/config_drift                         api_config_drift
 14980  GET              /api/system/config_snapshot                      api_system_config_snapshot
 15191  GET              /api/system/preflight                            api_system_preflight
 15317  GET              /api/system/preflight_history                    api_system_preflight_history
 15638  GET              /api/system/resilience                           api_system_resilience
 16767  GET              /api/tags                                        api_tags_list
 10924  GET              /api/top                                         api_top
 13134  GET              /api/trackings                                   api_trackings
 17560  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 17611  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 16803  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 17016  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 17640  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 16789  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15828  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15875  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 15904  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 15886  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 11117  POST             /api/trackings/bulk                              api_trackings_bulk
 15843  GET              /api/trackings/export                            api_trackings_export
 16771  GET              /api/trackings/tags-map                          api_trackings_tags_map
 17071  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11936  GET              /api/trend-7d                                    api_trend_7d
 25062  GET              /api/tts/<fn>                                    api_tts_file
 13394  POST             /api/tunnel/set                                  api_tunnel_set
 13373  GET              /api/tunnel/status                               api_tunnel_status
 13405  POST             /api/tunnel/test                                 api_tunnel_test
 13386  POST             /api/tunnel/toggle                               api_tunnel_toggle
 18380  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 18357  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 18339  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 26202  GET              /api/upload_window                               api_upload_window
 11194  GET              /api/userstats                                   api_userstats
 14423  GET              /api/version                                     api_version
 17679  GET/POST         /api/webhooks                                    api_webhooks
 17719  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete
 17750  POST             /api/webhooks/<int:wid>/test                     api_webhook_test
 17734  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle
 18236  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 18257  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 18221  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 18205  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 31329  GET              /api/youtube/sendrate                            api_youtube_sendrate
 16281  GET              /archive/<int:eid>/download                      archive_download
 16448  GET              /download/<int:recording_id>                     download
 15950  GET              /health                                          health
 24511  GET              /healthz                                         healthz
 10751  GET              /login                                           dashboard_login_page
 10785  GET              /logout                                          dashboard_logout
 10792  GET              /manifest.webmanifest                            pwa_manifest
 15008  GET              /metrics                                         api_prometheus_metrics
 26011  GET              /overlay                                         overlay_page
 10816  GET              /pwa-icon-<variant>.png                          pwa_icon
 10802  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (34)

```
   814  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   896  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   924  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   935  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   801  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   863  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   850  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   831  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   476  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   471  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   519  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   402  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   729  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   493  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   456  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   429  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   573  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   662  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   568  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   501  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   281  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   746  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   369  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   624  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   779  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   764  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   325  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   563  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   549  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   532  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   589  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   682  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   578  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
```

## Discord-Slash-Commands (45)

```
 28354  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 28813  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 28445  /assign_role            Rolle/Gruppe einem Mitglied geben
 28491  /ban                    Mitglied bannen
 29145  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 29069  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 29109  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 29094  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 28936  /clips                  Letzte Highlight-Clips eines Users
 28406  /create_category        Kategorie anlegen
 28375  /create_channel         Text-Channel anlegen (optional in Kategorie)
 28434  /create_group           Nutzergruppe (= Rolle) anlegen
 28417  /create_role            Rolle / Nutzergruppe anlegen
 28391  /create_voice           Voice-Channel anlegen
 28727  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 28843  /event                  Community-Event ankündigen (Admin) — mit Countdown
 28886  /events                 Kommende Community-Events anzeigen
 28982  /follow                 Bei Live-Gang eines Streamers gepingt werden
 28966  /help                   Alle Bot-Befehle anzeigen
 28480  /kick                   Mitglied kicken
 28709  /leaderboard            Top-10 der Community nach XP
 28922  /livenow                Welche getrackten User sind gerade live
 28952  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 28783  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 28515  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 28695  /rank                   Dein Level und Rang anzeigen
 28909  /recstatus              Aktuell laufende Aufnahmen
 28456  /remove_role            Rolle/Gruppe entfernen
 28368  /restream_status        Restream-Status
 28467  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 28660  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 28678  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 29008  /stats                  Statistik zu einem getrackten Streamer
 28280  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 29304  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 29201  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 29177  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 28502  /timeout                Mitglied stummschalten (Minuten)
 29080  /topstreamers           Rangliste der Streamer nach Aufnahmen
 28310  /track                  TikTok-User tracken
 28294  /tracklist              Getrackte TikTok-User dieses Servers
 28997  /unfollow               Live-Pings für einen Streamer abbestellen
 28343  /untrack                TikTok-User nicht mehr tracken
 29030  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 29054  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 29788  on_member_join
 29750  on_message
 29391  on_raw_reaction_add
 29823  on_ready
```

## Top-Level-Symbole in bot_v37.py (569 Funktionen, 2 Klassen)

```
  2366-2367   _abo_key
  2387-2405   _abo_probe_dump
 27191-27201  _active_recorder_sync
 21486-21493  _ad_allowlist
 22599-22605  _agent_for
 27203-27221  _ai_calls_total_sync
 13047-13057  _ai_dashboard_rate_check
 22608-22624  _ai_telemetry
 23106-23124  _alert
 29936-29986  _alert_monitor_loop
 30360-30422  _announce_loop
  3308-3317   _anthropic_key
  3337-3349   _anthropic_model
  3320-3331   _anthropic_model_raw
  3952-3962   _archive_open_unique
 10554-10557  _arg_int
  2358-2363   _as_dict
 19692-19697  _audio_cfg
 23260-23282  _audio_tap_cmd
 10687-10698  _auth_cookie
 10654-10683  _auth_guard
  1514-1519   _auto_on
 24149-24167  _auto_restream_loop
 31490-31505  _azrael_broadcast_reply
 31390-31412  _azrael_chat_reply
 31373-31387  _azrael_chat_should_reply
 13966-13984  _azrael_creator_take
 31418-31420  _azrael_gate_cfg
 22629-22643  _azrael_live_state
 25910-25924  _azrael_overlay_state
 22989-23043  _azrael_proactive_loop
 22448-22504  _azrael_reaction_to_chats
 31423-31430  _azrael_reply_all_chats
 31360-31370  _azrael_self_names
 31458-31487  _azrael_send_to
 22646-22667  _azrael_system
 30100-30103  _backup_active
 30181-30194  _backup_loop
 21374-21375  _badwords_path
 29901-29910  _brain_growth_loop
 12012-12039  _brain_growth_snapshot
  2294-2314   _brain_hint_delay
 12004-12006  _brain_history_for
  7125-7153   _brain_notify
 11981-12002  _brain_record
 12008-12010  _brain_stream_recent
 15552-15569  _browser_push
 11454-11474  _build_context_for_llm
  7169-7256   _build_daily_summary
  2797-2977   _build_native_cmd
 20040-20227  _build_restream_cmd
  3021-3054   _build_ytdlp_cmd
 27143-27150  _cached_probe
  5947-5974   _can_stop_tracking
  1694-1716   _capture_set_cookies
 17119-17131  _cfg_get
 17134-17141  _cfg_set
 25654-25689  _channel_set_all
 19290-19293  _chat_connected
 19296-19312  _chat_disconnected
  9151-9162   _chat_is_forum
 19332-19334  _chat_sanitize
 19336-19345  _chat_src_ok
 19275-19287  _chat_stat
 19315-19318  _chat_stats_snapshot
  3691-3702   _check_ai_alive_sync
  3705-3717   _check_ai_models_sync
 27152-27165  _check_redis_alive_sync
 27167-27187  _check_redis_version_sync
 12742-12785  _classify_pool_anonymity
 12788-12805  _classify_pool_anonymity_bg
   746-750    _claude_chat_sync_metered
 10579-10586  _client_ip
 30454-30481  _clip_prune
 30484-30494  _clip_recfile_for
 31010-31016  _clip_should_velocity
 30535-30617  _clip_to_discord
  3510-3519   _close_ai_session
 31534-31549  _cohost_broadcast
 31516-31520  _cohost_cfg
 31575-31587  _cohost_fire_highlight
 31523-31531  _cohost_gate
 31552-31572  _cohost_highlight
 30666-30700  _community_events_loop
 11397-11433  _conv_add_message
 11436-11441  _conv_archive
 11372-11381  _conv_create
 11386-11394  _conv_messages
 11444-11451  _conv_rename
  7549-7589   _cookie_alarm_loop
  1766-1770   _cookie_autorefresh_info
  1671-1675   _cookie_header
 15602-15634  _cpu_load_snapshot
  3899-3911   _create_index_safe
 13934-13949  _creator_activity
 13990-14013  _creator_dossier_generate
 13952-13963  _creator_facts_line
 27404-27510  _crowdsec_status
 27370-27401  _crowdsec_via_lapi
 27235-27253  _cscli_bin
 27259-27272  _cscli_path
  7442-7467   _daily_summary_loop
 27290-27307  _darf_journal_lesen
 29913-29933  _db_maintenance_loop
  7414-7439   _db_vacuum_loop
 21509-21533  _detect_foreign_ad
  1271-1282   _diag_path_owner
 22895-22939  _director_finalize
 23706-23713  _director_for
 22844-22892  _director_mark
 30904-30939  _disc_automod_check
 30877-30883  _disc_state_get
 30886-30893  _disc_state_set
 27953-27966  _discord_guild_filesize_bytes
 28152-28161  _discord_invite
 30838-30874  _discord_live_thread
 23046-23058  _discord_notify
 28053-28078  _discord_ops_alert
 30736-30834  _discord_post_user
 28217-29898  _discord_run_once
 28091-28149  _discord_start
 30425-30431  _discord_stop
 27974-27976  _discord_upload_limit_label
 27969-27971  _discord_upload_limit_mb
  7470-7544   _disk_alarm_loop
 32803-32852  _disk_autoclean
 32855-32868  _disk_guard_loop
 32795-32800  _disk_pct
 25967-25970  _donations_unknown_count
 19649-19651  _drawtext_chain
 16545-16547  _dump_all_threads
 12667-12731  _enrich_proxies_with_geo
  1911-1955   _ensure_cookie_file_netscape
 28164-28214  _ensure_discord_invite
 30631-30663  _ensure_error_channel
 12910-12947  _ensure_proxy_ready
  9164-9187   _ensure_topic
   627-629    _env_int
   632-634    _env_int_range
 30703-30733  _error_channel_loop
 23090-23103  _event_webhook
 18583-18589  _evo_build_dir
 18592-18599  _evo_version
 18875-18956  _evolution_cycle
 18608-18628  _evolution_llm_note
 18959-18969  _evolution_loop
 18631-18872  _evolution_write_build
  6567-6601   _extract_file_payload
  2043-2045   _extract_urls_from_streamurl_node
 27275-27282  _f2b_sudo_hint
 23126-23128  _faster_whisper_available
 21398-21410  _fetch_ldnoobw_de
 12556-12574  _fetch_proxy_list
 23540-23568  _fetch_tiktok_room_id
   678-681    _ff_cmd
 17256-17269  _ffmpeg_version_str
 19812-19817  _find_chromium
  3014-3018   _find_external_recorder
  2048-2050   _find_stream_urls
 17184-17209  _fire_webhooks
  8325-8334   _fork_safe
   761-770    _freeai_chat_sync_metered
 27325-27367  _geo_lookup_ips
  3499-3508   _get_ai_session
  8159-8199   _get_live_info
  2584-2591   _get_resolve_semaphore
  8513-8878   _handle_single_tracking
 32647-32649  _hb
 32652-32669  _hb_while
 19350-19352  _highlight_cfg
 19355-19384  _highlight_observe
 19820-19825  _htmlov_screenshot_cmd
 23284-23294  _httpx_proxy
 17217-17229  _in_quiet_hours
 33636-33667  _install_fast_eventloop
 10449-10503  _install_fast_json
 16550-16566  _install_faulthandler
 24392-24401  _intel_ensure_schema
 24426-24457  _intel_index_loop
 24413-24423  _intel_index_one
 24404-24410  _intel_semantic
  5936-5945   _is_authorized
  8443-8449   _is_dead
  2033-2035   _is_hevc
 27310-27316  _is_private_ip
  1417-1424   _is_process_running
  7155-7166   _is_quiet_hours
  1079-1088   _is_upload_window
 10538-10551  _json_error_handler
  7372-7402   _kick_broadcaster_id
 13440-13459  _kick_channel_live
  7289-7331   _kick_follower_count
 14502-14515  _kick_oauth_exchange
 14518-14520  _kick_oauth_page
 14461-14465  _kick_redirect_public
 14452-14458  _kick_redirect_source
 14438-14449  _kick_redirect_uri
  7274-7276   _kick_slug
 14468-14499  _kick_user_token
  3968-3976   _kind_from_filename
 17246-17251  _latest_popularity
 21420-21426  _learned_load
 21417-21418  _learned_path
 21428-21436  _learned_save
 23921-23951  _live_react_loop
 23717-23910  _live_react_worker
 22507-22518  _live_transcript_push
 23912-23919  _live_users
 22942-22986  _living_title_loop
  3562-3572   _llm_list_models
 21377-21385  _load_banned_words_file
  1592-1665   _load_cookies_dict
 30106-30178  _local_backup_scan
 10520-10534  _log_5xx
 20235-20239  _looks_like_codec_err
 20230-20232  _looks_like_source_expired
  8406-8436   _loop_fehler
 16570-16579  _loop_heartbeat
 32617-32644  _loop_lag_monitor
 16689-16692  _loop_not_ready
 16582-16650  _loop_watchdog_thread
 22387-22401  _loyalty_add
 22378-22384  _loyalty_get
 22404-22412  _loyalty_top
 17980-17998  _manual_donations_rows
 18001-18003  _manual_donations_total
  8451-8452   _mark_dead
 13607-13636  _marketing_cfg
 13598-13604  _marketing_default_targets
 13593-13595  _marketing_enabled
 13650-13665  _marketing_flavor
 13720-13736  _marketing_loop
 13668-13678  _marketing_post_discord
 13681-13693  _marketing_post_telegram
 13696-13717  _marketing_publish
 13639-13643  _marketing_state_obj
 13646-13647  _marketing_state_save
 31437-31455  _maybe_handle_command
 32954-32978  _maybe_hype_clip
  3866-3889   _migrate_columns
 31712-31723  _mod_is_exempt
 31726-31731  _mod_warn_first
 31734-31737  _mod_warn_text
 19138-19146  _modlog
   883-885    _multistream_targets
  8337-8338   _nc_create_subprocess_exec
  8341-8342   _nc_create_subprocess_shell
 13831-13847  _news_cfg
 13818-13820  _news_enabled
 13885-13926  _news_facts
 14040-14062  _news_generate
 14245-14262  _news_loop
 13823-13828  _news_output_path
 13929-13931  _news_phrase
 14016-14037  _news_phrase_impl
 13860-13867  _news_read
 13850-13853  _news_state_obj
 13856-13857  _news_state_save
 13870-13882  _news_write
 26295-26319  _nl_to_sql
 19176-19178  _normalize_ingest
  2225-2242   _note_check_duration
 22533-22541  _oracle_memories
 22799-22833  _oracle_memorize
 22544-22557  _oracle_persona
 22526-22530  _oracle_recent_text
 19475-19483  _ov_atomic_write
 19463-19469  _ov_bar
 21333-21345  _ov_clip_text
 19472-19473  _ov_oneline
 25978-26007  _overlay_push
 19766-19809  _overlay_render_size
 19237-19241  _overlay_session_reset
 25926-25929  _overlay_src_ok
 21496-21506  _own_invites
 17961-17977  _parse_eur
 19761-19763  _parse_size
 27518-27598  _parse_ssh_attacks
  7761-7794   _pause_resume_cmd
  1720-1764   _persist_refreshed_cookies
  1558-1590   _pick_checked_pull_proxy
 10606-10611  _pin_auth_value
 10643-10644  _pin_clear_fail
 10623-10626  _pin_locked
 10629-10640  _pin_note_fail
 10614-10620  _pin_ok
 25816-25818  _piper_available
 25781-25803  _piper_list_voices
 25823-25848  _piper_pick_model
 25860-25907  _piper_say
 25774-25778  _piper_voice_roots
 17146-17181  _post_json_threaded
 19740-19758  _probe_video_size
  1445-1462   _proc_is_recorder
 12654-12665  _proxy_geo_cache_put
 12881-12907  _proxy_pool_refresh_loop
  1524-1555   _proxy_report_recording
 16535-16537  _prune_stall_dumps
 14065-14186  _public_stats
 23061-23087  _push_notify
 10745-10747  _pwa_dir
 12625-12640  _quick_validate_proxy
 17212-17214  _quiet_hours_config
 10710-10743  _rate_guard
 22352-22358  _react_warn
  8245-8284   _reap_proc
  2265-2287   _record_check_outcome
   673-675    _redact_stream_urls
 12808-12878  _refresh_proxy_pool
 25806-25812  _resolve_piper_model
  2059-2149   _resolve_via_html
  2407-2561   _resolve_via_webcast_api_v2
  2624-2686   _resolve_via_ytdlp
 31056-31185  _resolve_youtube_ingest
 23990-23997  _restream_active_platforms
 19222-19233  _restream_active_sources
 23571-23670  _restream_chat_guardian
 19387-19459  _restream_chat_push
 19149-19161  _restream_enabled
 19828-19915  _restream_html_overlay_start
 19918-19931  _restream_html_overlay_stop
  1027-1029   _restream_layout_mode
 19187-19210  _restream_overlay_files
 23955-23987  _restream_platform_state
 24111-24146  _restream_resume_after_restart
 19979-20037  _restream_tts_enqueue_wav
 19702-19734  _restream_tts_feeder
 19699-19700  _restream_tts_fifo_path
 19934-19961  _restream_tts_start
 19963-19977  _restream_tts_stop
 24000-24108  _restream_verify_loop
 30071-30083  _retention_loop
 30030-30068  _retention_scan
  2369-2371   _room_is_abo
  6605-6722   _run_ai_call
 16673-16686  _run_async_from_flask
 27319-27322  _run_priv
 33624-33632  _run_selfcheck_and_exit
 30086-30097  _s3_client
 26259-26290  _safe_select
  8454-8500   _safe_send
  5088-5104   _sample_net_throughput
 21387-21395  _save_banned_words_file
  2317-2344   _schedule_next_check
 29989-30027  _scheduler_loop
  3892-3896   _schema_pk
 16694-16699  _scraper_session
 31740-31779  _screen_full
 14828-14865  _sec_headers
  2038-2040   _select_stream_from_data_section
 33437-33621  _selfcheck
  1102-1106   _should_defer_upload
 30497-30532  _shrink_for_discord
 32875-32892  _sign_health_check
 32895-32914  _sign_health_loop
  8354-8365   _spawn
  8368-8398   _spawn_from_flask
 27642-27645  _st_befund
 23296-23537  _start_chat_listener
 16653-16670  _start_loop_watchdog
 14210-14236  _stats_loop
 14189-14192  _stats_output_path
 14195-14207  _stats_write
  8946-8960   _storage_cleanup_loop
 32934-32941  _story_for
  3076-3082   _stream_url_expiry
  3091-3097   _stream_url_is_fresh
  3084-3089   _stream_url_ttl
 21460-21467  _streamer_persona_get
 21442-21448  _streamer_personas_load
 21439-21440  _streamer_personas_path
 21450-21458  _streamer_personas_save
 19654-19658  _studio_chain
 30203-30325  _system_backup
 30328-30356  _system_backup_loop
 12577-12616  _test_proxy
 13481-13490  _testpush_cfg
 13493-13510  _testpush_exec
 13462-13478  _testpush_resolve_live
  9123-9133   _tg_topics_load_into_mem
  9120-9121   _tg_topics_path
  9135-9142   _tg_topics_save
 26852-26900  _tiktok_account_exists
 10589-10597  _token_ok
  9145-9149   _topic_forget
 17232-17243  _tracking_max_duration
  1329-1352   _try_attach_file_handler
 25850-25858  _tts_cleanup
 13366-13369  _tunnel_effective
 25276-25329  _twitch_channel_status
 31782-31924  _twitch_chat_loop
 31598-31699  _twitch_eventsub_loop
 18401-18404  _twitch_oauth_page
  1125-1138   _upload_queue_add
  1149-1151   _upload_queue_count
  1108-1117   _upload_queue_load
  1098-1100   _upload_queue_path
  1140-1147   _upload_queue_remove
  1119-1123   _upload_queue_save
  1153-1191   _upload_window_loop
  8218-8225   _uptime_s
 19164-19173  _url_host
   739-743    _usage_record_claude
  7334-7362   _viewer_sample_loop
  7404-7411   _viewer_stats
 10647-10650  _wants_html
  8228-8242   _warn_empty_env
 32690-32785  _watchdog_loop
 31339-31347  _wchat_thank_ok
 23130-23160  _whisper_get_model
  8315-8322   _whisper_native_section
 22339-22345  _whisper_pool
 23229-23258  _whisper_segments
 23162-23226  _whisper_transcribe
 19485-19647  _write_restream_overlay
 31952-32025  _youtube_api_chat_loop
 25332-25435  _youtube_api_status
 25438-25505  _youtube_channel_status
 32028-32185  _youtube_chat_loop
 31191-31204  _youtube_restream_autoconfig
 31207-31231  _youtube_restream_autoconfig_inner
 31297-31325  _youtube_send
 25610-25651  _youtube_set_channel
 31234-31268  _yt_access_token
 31271-31286  _yt_live_chat_id
 31945-31949  _yt_oauth_configured
 31292-31294  _yt_sendrate_cfg
 31927-31942  _yt_timeout
  2608-2609   _ytdlp_detect_available
  2611-2622   _ytdlp_note_result
 16540-16542  _zombie_child_count
  8095-8119   about
  4339-4358   add_ai_log_entry
  4227-4235   add_archive_entry
  5201-5216   add_archive_rule
  4783-4817   add_recording
  4444-4461   add_tracking
  4878-4895   add_tracking_tag
  6725-6758   ai
  3731-3770   ai_chat
  3804-3814   ai_history_append
  3816-3821   ai_history_clear
  3793-3802   ai_history_load
  3778-3791   ai_rate_limit_check
  6787-6795   aireset
  3941-3949   archive_writeable
 22670-22689  azrael_chat
 32190-32312  brain_cmd
  3100-3284   build_recording_cmd
  4464-4541   bulk_add_trackings
  4032-4072   bulk_delete_archive_entries
  7592-7651   bulkadd
  8963-9103   check_all_trackings
  4628-4640   claim_live_transition
 21536-22282  class KickModerator
 20242-21220  class RestreamManager
 12992-13034  classify_proxy_anonymity
  6833-7031   cleanup
  5796-5837   cleanup_old_recordings
  4774-4781   clear_recording
 30942-31007  clip_moment
  5349-5392   cluster_failures
  5032-5081   compute_storage_forecast
  7714-7758   cookies_cmd
  5638-5644   cookies_days_old
  4435-4441   count_trackings_for_chat
  4326-4337   decide_preferred_recorder
  4245-4269   delete_archive_entry
  5218-5226   delete_archive_rule
  6262-6409   diag
 32315-32376  einnahmen_cmd
  5026-5029   find_recordings_by_fingerprint
  4287-4303   finish_recording_attempt
  4573-4583   get_all_active_trackings
  4380-4383   get_all_checks
  4819-4822   get_all_recordings
  4920-4930   get_all_tags_with_counts
  5003-5006   get_annotations_for_recording
  3987-3999   get_archive_aggregate_stats
  4237-4243   get_archive_entry
  4001-4013   get_archive_kind_breakdown
  4016-4030   get_archive_missing_ids
  4996-4999   get_bookmarked_recordings
  1787-1904   get_cookie_health
  4869-4875   get_event_log
  4310-4324   get_last_recording_attempt
  2689-2794   get_live_status
  5552-5555   get_manual_recordings
  5011-5014   get_or_compute_inspect_sync
  5872-5916   get_outcome_breakdown
  4977-4985   get_priority_poll_interval
  5179-5188   get_profile_snapshots
  4360-4370   get_recent_ai_log
  4305-4308   get_recent_recording_attempts
  4824-4827   get_recording_by_id
  4989-4992   get_recording_note
  3447-3470   get_redis
  4411-4427   get_stats
  5763-5794   get_storage_stats
  4910-4918   get_tags_for_tracking
  5319-5333   get_tiktok_status_distribution
  4964-4975   get_tracking_priority
  4642-4651   get_tracking_state
  4569-4571   get_trackings_for_group
  5568-5571   get_trash_recordings
  9807-10417  handle_recording_finished
  3914-3939   init_db
  5686-5740   inspect_stream_url
 25973-25975  is_revenue_platform
  5191-5199   list_archive_rules
  6066-6104   live
  8503-8511   live_check_worker
  3522-3556   llm_chat
  3621-3688   llm_chat_stream_sync
  3590-3618   llm_chat_sync
  3575-3587   llm_list_models
  4835-4861   log_event
  1379-1412   log_recording_failure
  7908-7957   logs_cmd
 32982-33427  main
  6761-6784   on_ai_media
  8034-8060   on_ai_reply
  8063-8092   on_azrael_mention
  8124-8154   on_callback
 22692-22796  oracle_handle
  7797-7800   pause_tracking
  5926-5931   profile_keyboard
  5647-5683   quick_restart_tracking
  7859-7905   quota
  8880-8943   reaper_loop
  5315-5317   record_tiktok_status
  6800-6830   recstatus
  3472-3480   redis_get_json
  3482-3488   redis_set_json
  4543-4567   remove_tracking
  4897-4908   remove_tracking_tag
  4087-4222   rename_archive_entry
 32379-32389  report_cmd
 13037-13039  report_proxy_result
  2152-2179   resolve_tiktok_live_stream
  5563-5566   restore_recording
  7803-7806   resume_tracking
  5229-5309   run_archive_rules
 32392-32597  run_bot
 16462-16509  run_flask
  5107-5152   sample_bandwidth_for_active
  5158-5177   save_profile_snapshot
  4372-4378   save_tiktok_check
  4766-4772   set_recording_file
  4586-4624   set_tracking_paused
  4933-4962   set_tracking_priority
  5558-5561   soft_delete_recording
  9192-9805   split_and_send_video
  5979-6021   start
  4271-4285   start_recording_attempt
  7034-7072   stats
  5533-5550   stop_manual_recording
  7809-7856   stoprec
  7259-7267   summary_cmd
  7960-8031   sysres
  6411-6555   teststream
  6023-6064   tiktok
  7654-7711   topusers
  6141-6198   track
  6106-6138   track_exact
  6212-6260   tracklist
  5399-5531   trigger_manual_recording
  4727-4764   try_acquire_recording_lock
  5574-5633   universal_search
  6200-6210   untrack
  5021-5024   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
archive.py             compute_recording_fingerprint, evaluate_archive_rule, get_archive_entries_paged, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              build_payload, chat_sync, is_retired, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           class MarketingConfig, class MarketingState, compose, has_content, next_due_ts, should_post, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                build_items, class NewsConfig, class NewsState, item_id, merge, render_json, should_generate
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
trackingdb.py          claim_transition, get_state
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
