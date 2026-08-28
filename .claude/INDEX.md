# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (262)

```
 10655  GET              /                                                dashboard
 15681  GET              /api/abo/status                                  api_abo_status
 10763  GET              /api/active-recordings                           api_active_recordings
 15756  GET              /api/activity-pulse                              api_activity_pulse
 15109  GET              /api/ai-log                                      api_ai_log
 11241  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15516  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23565  GET/POST         /api/audio/config                                api_audio_config
 23595  POST             /api/audio/testtone                              api_audio_testtone
 15622  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15646  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15650  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12519  GET              /api/automation/status                           api_automation_status
 12541  POST             /api/automation/toggle                           api_automation_toggle
 14267  GET              /api/azrael/agents                               api_azrael_agents
 12422  POST             /api/azrael/ask                                  api_azrael_ask
 23801  GET/POST         /api/azrael/context                              api_azrael_context
 13894  GET              /api/azrael/core                                 api_azrael_core
 23935  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23925  GET              /api/azrael/live_status                          api_azrael_live_status
 23943  POST             /api/azrael/live_test                            api_azrael_live_test
 14276  GET              /api/azrael/memories                             api_azrael_memories
 23991  POST             /api/azrael/persona                              api_azrael_persona_set
 23982  GET              /api/azrael/personas                             api_azrael_personas
 24019  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23774  POST             /api/azrael/react                                api_azrael_react
 23810  GET              /api/azrael/reaction                             api_azrael_reaction
 23962  GET              /api/azrael/reactions                            api_azrael_reactions
 24012  GET              /api/azrael/transcript                           api_azrael_transcript
 23897  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23872  GET              /api/azrael/voices                               api_azrael_voices
 24036  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11336  GET              /api/backoff-watch                               api_backoff_watch
 14880  POST             /api/backup/run                                  api_backup_run
 14846  GET              /api/backup/status                               api_backup_status
 14835  POST             /api/backup/system                               api_backup_system
 15588  GET              /api/bandwidth/live                              api_bandwidth_live
 15501  GET              /api/bookmarks                                   api_bookmarks_list
 11599  GET              /api/brain                                       api_brain
 11536  GET              /api/brain/alarms                                api_brain_alarms
 11521  GET              /api/brain/creator                               api_brain_creator
 11498  GET              /api/brain/graph                                 api_brain_graph
 11559  GET              /api/brain/growth                                api_brain_growth
 10209  GET              /api/brain/health                                api_brain_health
 24517  GET              /api/channel/categories                          api_channel_categories
 24523  POST             /api/channel/set                                 api_channel_set
 24333  GET              /api/channels/status                             api_channels_status
 23166  POST             /api/chat/send                                   api_chat_send
 14534  GET              /api/chat/send_status                            api_chat_send_status
 10744  GET              /api/checks                                      api_checks
 23838  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23821  GET              /api/clips                                       api_clips
 23854  POST/DELETE      /api/clips/clear                                 api_clips_clear
 23440  GET              /api/cohost                                      api_cohost
 23452  POST             /api/cohost/config                               api_cohost_config
 16320  GET              /api/community/stats                             api_community_stats
 25517  POST             /api/config/restore                              api_config_restore
 25502  GET              /api/config/snapshot                             api_config_snapshot
 15779  GET              /api/cookies/age                                 api_cookies_age
 10811  GET              /api/cookies/health                              api_cookies_health
 10818  POST             /api/cookies/update                              api_cookies_update
 25468  GET              /api/data/export                                 api_data_export
 16835  GET              /api/db/export                                   api_db_export
 16862  POST             /api/db/import                                   api_db_import
 16822  GET              /api/db/summary                                  api_db_summary
 23366  GET              /api/debug/threads                               api_debug_threads
 26403  GET              /api/defense/attacks                             api_defense_attacks
 26370  GET              /api/defense/crowdsec                            api_defense_crowdsec
 26388  GET              /api/defense/fail2ban                            api_defense_fail2ban
 26094  GET              /api/defense/overview                            api_defense_overview
 14942  POST             /api/discord/announce                            api_discord_announce
 14670  GET              /api/discord/clips_week                          api_discord_clips_week
 14886  GET              /api/discord/community                           api_discord_community
 14562  GET              /api/discord/invite                              api_discord_invite
 14025  GET              /api/discord/overview                            api_discord_overview
 14111  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16397  POST             /api/donations/add                               api_donations_add
 16430  GET              /api/donations/manual                            api_donations_manual
 16438  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16333  POST             /api/donations/reset                             api_donations_reset
 16454  GET              /api/donations/summary                           api_donations_summary
 15570  GET              /api/events                                      api_events
 14717  GET              /api/events/stream                               api_events_stream
 17588  GET              /api/evolution/changelog                         api_evolution_changelog
 17573  GET              /api/evolution/history                           api_evolution_history
 17513  GET              /api/evolution/learned                           api_evolution_learned
 17535  GET              /api/evolution/proposals                         api_evolution_proposals
 17556  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17503  POST             /api/evolution/run                               api_evolution_run
 17603  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17468  GET              /api/evolution/status                            api_evolution_status
 16669  GET              /api/finanzamt/entries                           api_finanzamt_entries
 16689  POST             /api/finanzamt/entry                             api_finanzamt_add
 16716  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15583  GET              /api/forecast/storage                            api_forecast_storage
 12557  GET              /api/freeai/status                               api_freeai_status
 13967  GET              /api/health                                      api_health
 15601  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15597  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23489  GET              /api/highlights                                  api_highlights
 23501  POST             /api/highlights/config                           api_highlights_config
 24374  GET              /api/kick/channel                                api_kick_channel
 24395  POST             /api/kick/channel                                api_kick_channel_set
 13694  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13762  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13740  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13679  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13719  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23613  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23682  POST             /api/kickmod/config                              api_kickmod_config
 23727  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23741  GET              /api/kickmod/learned                             api_kickmod_learned
 23768  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23748  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 24079  POST             /api/kickmod/say                                 api_kickmod_say
 24055  POST             /api/kickmod/start                               api_kickmod_start
 23653  GET              /api/kickmod/status                              api_kickmod_status
 24066  POST             /api/kickmod/stop                                api_kickmod_stop
 10589  POST             /api/login                                       dashboard_login_submit
 16305  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12972  POST             /api/marketing/config                            api_marketing_config
 12997  GET              /api/marketing/preview                           api_marketing_preview
 13007  POST             /api/marketing/send-now                          api_marketing_send_now
 12946  GET              /api/marketing/status                            api_marketing_status
 12964  POST             /api/marketing/toggle                            api_marketing_toggle
 23516  GET              /api/moderation/feed                             api_moderation_feed
 13525  POST             /api/news/config                                 api_news_config
 13491  GET              /api/news/creators                               api_news_creators
 13502  POST             /api/news/creators/generate                      api_news_creators_generate
 13567  POST             /api/news/generate-now                           api_news_generate_now
 13562  GET              /api/news/items                                  api_news_items
 13553  GET              /api/news/preview                                api_news_preview
 13472  GET              /api/news/status                                 api_news_status
 13517  POST             /api/news/toggle                                 api_news_toggle
 16162  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14499  GET              /api/notify/status                               api_notify_status
 14510  POST             /api/notify/test                                 api_notify_test
 14485  GET              /api/ops/audit                                   api_ops_audit
 16233  GET              /api/ops/db-stats                                api_ops_db_stats
 16261  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14291  GET              /api/ops/errors                                  api_ops_errors
 16182  GET              /api/ops/healthcheck                             api_ops_healthcheck
 17015  GET              /api/ops/log-tail                                api_ops_log_tail
 12402  GET              /api/ops/logtail                                 api_ops_logtail
 14232  GET              /api/ops/metrics                                 api_ops_metrics
 14215  GET              /api/ops/resource_history                        api_ops_resource_history
 16891  GET              /api/ops/version                                 api_ops_version
 11094  GET              /api/outcomes                                    api_outcomes
 24998  POST             /api/overlay/config                              api_overlay_config
 24985  POST             /api/overlay/event                               api_overlay_event
 24890  GET              /api/overlay/state                               api_overlay_state
 11127  GET              /api/profile/<username>                          api_profile
 15787  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15609  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15735  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15712  GET              /api/proxy/trend                                 api_proxy_trend
 13446  GET              /api/public/stats                                api_public_stats
 10689  GET              /api/pulse                                       api_pulse
 15133  GET              /api/recording-attempts                          api_recording_attempts
 23101  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 23079  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 23120  POST             /api/restream/<int:rid>/start                    api_restream_start
 23387  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24852  GET              /api/restream/chatfeed                           api_restream_chatfeed
 23055  POST             /api/restream/create                             api_restream_create
 13770  GET              /api/restream/deck                               api_restream_deck
 12493  GET              /api/restream/health                             api_restream_health
 24874  POST             /api/restream/layout                             api_restream_layout
 23028  GET              /api/restream/list                               api_restream_list
 12466  POST             /api/restream/report                             api_restream_report
 23400  POST             /api/restream/start_all                          api_restream_start_all
 23426  POST             /api/restream/stop_all                           api_restream_stop_all
 12720  GET              /api/restream/testpush                           api_testpush_status
 12745  POST             /api/restream/testpush                           api_testpush_run
 16570  GET              /api/restream/verify                             api_restream_verify
 14648  GET              /api/retention/preview                           api_retention_preview
 14657  POST             /api/retention/run                               api_retention_run
 25583  POST             /api/schedule/add                                api_schedule_add
 25573  GET              /api/schedule/list                               api_schedule_list
 25608  POST             /api/schedule/remove                             api_schedule_remove
 15486  GET              /api/search                                      api_search
 26141  GET              /api/selftest                                    api_selftest
 23137  GET              /api/shield/stats                                api_shield_stats
 10708  GET              /api/stats                                       api_stats
 15750  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15677  GET              /api/stats/tiktok-status                         api_tiktok_status
 25548  GET              /api/stats/timeline                              api_stats_timeline
 10785  GET              /api/storage                                     api_storage
 10792  POST             /api/storage/cleanup                             api_storage_cleanup
 15663  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12443  GET              /api/stream/timeline                             api_stream_timeline
 14099  GET              /api/stream/transcript                           api_stream_transcript
 25216  GET              /api/streamer/compare                            api_streamer_compare
 25415  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14609  GET              /api/streamer/detail                             api_streamer_detail
 25440  GET              /api/streamer/digest/<username>                  api_streamer_digest
 25320  GET              /api/streamer/dormant                            api_streamer_dormant
 25396  GET              /api/streamer/exists/<username>                  api_streamer_exists
 25275  GET              /api/streamer/journal/<username>                 api_streamer_journal
 25240  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 25300  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13934  GET              /api/streamers/wall                              api_streamers_wall
 10934  GET              /api/summary/preview                             api_summary_preview
 15198  GET              /api/system                                      api_system
 16518  GET              /api/system/check_timing                         api_check_timing
 16803  GET              /api/system/config_drift                         api_config_drift
 14135  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14346  GET              /api/system/preflight                            api_system_preflight
 14472  GET              /api/system/preflight_history                    api_system_preflight_history
 14782  GET              /api/system/resilience                           api_system_resilience
 15521  GET              /api/tags                                        api_tags_list
 10758  GET              /api/top                                         api_top
 12376  GET              /api/trackings                                   api_trackings
 16051  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 16084  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15557  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15770  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 16113  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15543  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 14972  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15019  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 15048  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 15030  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 11020  POST             /api/trackings/bulk                              api_trackings_bulk
 14987  GET              /api/trackings/export                            api_trackings_export
 10989  GET              /api/trackings/groups                            api_trackings_groups
 15525  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15825  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11391  GET              /api/trend-7d                                    api_trend_7d
 23886  GET              /api/tts/<fn>                                    api_tts_file
 12600  POST             /api/tunnel/set                                  api_tunnel_set
 12579  GET              /api/tunnel/status                               api_tunnel_status
 12611  POST             /api/tunnel/test                                 api_tunnel_test
 12592  POST             /api/tunnel/toggle                               api_tunnel_toggle
 16775  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16752  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16734  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 16963  GET              /api/update/backups                              api_update_backups
 16929  GET              /api/update/check                                api_update_check
 16988  POST             /api/update/restart                              api_update_restart
 16968  POST             /api/update/rollback                             api_update_rollback
 16951  POST             /api/update/start                                api_update_start
 16944  GET              /api/update/status                               api_update_status
 25026  GET              /api/upload_window                               api_upload_window
 11108  GET              /api/userstats                                   api_userstats
 13578  GET              /api/version                                     api_version
 16631  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16652  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16616  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16600  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 29821  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15171  GET              /archive/<int:eid>/download                      archive_download
 15228  GET              /download/<int:recording_id>                     download
 15094  GET              /health                                          health
 23335  GET              /healthz                                         healthz
 10580  GET              /login                                           dashboard_login_page
 10610  GET              /logout                                          dashboard_logout
 10617  GET              /manifest.webmanifest                            pwa_manifest
 14163  GET              /metrics                                         api_prometheus_metrics
 24835  GET              /overlay                                         overlay_page
 10641  GET              /pwa-icon-<variant>.png                          pwa_icon
 10627  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (90)

```
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
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
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 26846  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 27305  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 26937  /assign_role            Rolle/Gruppe einem Mitglied geben
 26983  /ban                    Mitglied bannen
 27637  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 27561  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27601  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 27586  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 27428  /clips                  Letzte Highlight-Clips eines Users
 26898  /create_category        Kategorie anlegen
 26867  /create_channel         Text-Channel anlegen (optional in Kategorie)
 26926  /create_group           Nutzergruppe (= Rolle) anlegen
 26909  /create_role            Rolle / Nutzergruppe anlegen
 26883  /create_voice           Voice-Channel anlegen
 27219  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 27335  /event                  Community-Event ankündigen (Admin) — mit Countdown
 27378  /events                 Kommende Community-Events anzeigen
 27474  /follow                 Bei Live-Gang eines Streamers gepingt werden
 27458  /help                   Alle Bot-Befehle anzeigen
 26972  /kick                   Mitglied kicken
 27201  /leaderboard            Top-10 der Community nach XP
 27414  /livenow                Welche getrackten User sind gerade live
 27444  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 27275  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 27007  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 27187  /rank                   Dein Level und Rang anzeigen
 27401  /recstatus              Aktuell laufende Aufnahmen
 26948  /remove_role            Rolle/Gruppe entfernen
 26860  /restream_status        Restream-Status
 26959  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 27152  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 27170  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 27500  /stats                  Statistik zu einem getrackten Streamer
 26772  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 27796  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 27693  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 27669  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 26994  /timeout                Mitglied stummschalten (Minuten)
 27572  /topstreamers           Rangliste der Streamer nach Aufnahmen
 26802  /track                  TikTok-User tracken
 26786  /tracklist              Getrackte TikTok-User dieses Servers
 27489  /unfollow               Live-Pings für einen Streamer abbestellen
 26835  /untrack                TikTok-User nicht mehr tracken
 27522  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 27546  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 28280  on_member_join
 28242  on_message
 27883  on_raw_reaction_add
 28315  on_ready
```

## Top-Level-Symbole in bot.py (558 Funktionen, 2 Klassen)

```
  2465-2466   _abo_key
  2486-2504   _abo_probe_dump
 25683-25693  _active_recorder_sync
 20325-20332  _ad_allowlist
 21447-21453  _agent_for
 25695-25713  _ai_calls_total_sync
 21456-21472  _ai_telemetry
 21954-21972  _alert
 28428-28478  _alert_monitor_loop
 28852-28914  _announce_loop
  3407-3410   _anthropic_key
  3417-3419   _anthropic_model
 10337-10340  _arg_int
  2457-2462   _as_dict
 18185-18190  _audio_cfg
 22108-22130  _audio_tap_cmd
 10501-10512  _auth_cookie
 10468-10497  _auth_guard
  1613-1618   _auto_on
 23004-23022  _auto_restream_loop
 29982-29997  _azrael_broadcast_reply
 29882-29904  _azrael_chat_reply
 29865-29879  _azrael_chat_should_reply
 13172-13190  _azrael_creator_take
 29910-29912  _azrael_gate_cfg
 21477-21491  _azrael_live_state
 24734-24748  _azrael_overlay_state
 21837-21891  _azrael_proactive_loop
 21296-21352  _azrael_reaction_to_chats
 29915-29922  _azrael_reply_all_chats
 29852-29862  _azrael_self_names
 29950-29979  _azrael_send_to
 21494-21515  _azrael_system
 28592-28595  _backup_active
 28673-28686  _backup_loop
 20213-20214  _badwords_path
 28393-28402  _brain_growth_loop
 11467-11494  _brain_growth_snapshot
  2393-2413   _brain_hint_delay
 11459-11461  _brain_history_for
  6829-6857   _brain_notify
 11436-11457  _brain_record
 11463-11465  _brain_stream_recent
 14696-14713  _browser_push
  6873-6960   _build_daily_summary
  2896-3076   _build_native_cmd
 18533-18720  _build_restream_cmd
  3120-3153   _build_ytdlp_cmd
 25635-25642  _cached_probe
  5651-5678   _can_stop_tracking
  1793-1815   _capture_set_cookies
 15873-15876  _cfg_get
 15879-15881  _cfg_set
 24478-24513  _channel_set_all
 17783-17786  _chat_connected
 17789-17805  _chat_disconnected
  8902-8913   _chat_is_forum
 17825-17827  _chat_sanitize
 17829-17838  _chat_src_ok
 17768-17780  _chat_stat
 17808-17811  _chat_stats_snapshot
  3682-3693   _check_ai_alive_sync
  3696-3708   _check_ai_models_sync
 25644-25657  _check_redis_alive_sync
 25659-25679  _check_redis_version_sync
 14574-14587  _ci_key
 12066-12109  _classify_pool_anonymity
 12112-12129  _classify_pool_anonymity_bg
   775-779    _claude_chat_sync_metered
 10362-10369  _client_ip
 28946-28973  _clip_prune
 28976-28986  _clip_recfile_for
 29502-29508  _clip_should_velocity
 29027-29109  _clip_to_discord
  3580-3589   _close_ai_session
 30026-30041  _cohost_broadcast
 30008-30012  _cohost_cfg
 30067-30079  _cohost_fire_highlight
 30015-30023  _cohost_gate
 30044-30064  _cohost_highlight
 29158-29192  _community_events_loop
 11290-11292  _conv_messages
  7253-7293   _cookie_alarm_loop
  1865-1869   _cookie_autorefresh_info
  1770-1774   _cookie_header
 14746-14778  _cpu_load_snapshot
  3890-3902   _create_index_safe
 13140-13155  _creator_activity
 13196-13219  _creator_dossier_generate
 13158-13169  _creator_facts_line
 25896-26002  _crowdsec_status
 25862-25893  _crowdsec_via_lapi
 25727-25745  _cscli_bin
 25751-25764  _cscli_path
  7146-7171   _daily_summary_loop
 25782-25799  _darf_journal_lesen
 10957-10985  _dashboard_track_group
 28405-28425  _db_maintenance_loop
  7118-7143   _db_vacuum_loop
 20348-20372  _detect_foreign_ad
  1352-1363   _diag_path_owner
 21743-21787  _director_finalize
 22554-22561  _director_for
 21692-21740  _director_mark
 29396-29431  _disc_automod_check
 29369-29375  _disc_state_get
 29378-29385  _disc_state_set
 26445-26458  _discord_guild_filesize_bytes
 26644-26653  _discord_invite
 29330-29366  _discord_live_thread
 21894-21906  _discord_notify
 26545-26570  _discord_ops_alert
 29228-29326  _discord_post_user
 26709-28390  _discord_run_once
 26583-26641  _discord_start
 28917-28923  _discord_stop
 26466-26468  _discord_upload_limit_label
 26461-26463  _discord_upload_limit_mb
  7174-7248   _disk_alarm_loop
 31408-31457  _disk_autoclean
 31460-31473  _disk_guard_loop
 31400-31405  _disk_pct
 24791-24794  _donations_unknown_count
 18142-18144  _drawtext_chain
 15325-15327  _dump_all_threads
 11991-12055  _enrich_proxies_with_geo
  2010-2054   _ensure_cookie_file_netscape
 26656-26706  _ensure_discord_invite
 29123-29155  _ensure_error_channel
 12234-12271  _ensure_proxy_ready
  8915-8938   _ensure_topic
   638-640    _env_int
   643-645    _env_int_range
 29195-29225  _error_channel_loop
 21938-21951  _event_webhook
 17076-17082  _evo_build_dir
 17085-17092  _evo_version
 17368-17449  _evolution_cycle
 17101-17121  _evolution_llm_note
 17452-17462  _evolution_loop
 17124-17365  _evolution_write_build
  6271-6305   _extract_file_payload
  2142-2144   _extract_urls_from_streamurl_node
 25767-25774  _f2b_sudo_hint
 21974-21976  _faster_whisper_available
 20237-20249  _fetch_ldnoobw_de
 11880-11898  _fetch_proxy_list
 22388-22416  _fetch_tiktok_room_id
   709-712    _ff_cmd
 15996-16009  _ffmpeg_version_str
 18305-18310  _find_chromium
  3113-3117   _find_external_recorder
  2147-2149   _find_stream_urls
 15924-15949  _fire_webhooks
  8029-8038   _fork_safe
   790-799    _freeai_chat_sync_metered
 25817-25859  _geo_lookup_ips
  3569-3578   _get_ai_session
  7863-7903   _get_live_info
  2683-2690   _get_resolve_semaphore
  8264-8629   _handle_single_tracking
 31252-31254  _hb
 31257-31274  _hb_while
 17843-17845  _highlight_cfg
 17848-17877  _highlight_observe
 18313-18318  _htmlov_screenshot_cmd
 22132-22142  _httpx_proxy
 15957-15969  _in_quiet_hours
 32241-32272  _install_fast_eventloop
 10232-10286  _install_fast_json
 15330-15346  _install_faulthandler
 23247-23256  _intel_ensure_schema
 23294-23325  _intel_index_loop
 23268-23278  _intel_index_one
 23259-23265  _intel_semantic
  5640-5649   _is_authorized
  8194-8200   _is_dead
  2132-2134   _is_hevc
 25802-25808  _is_private_ip
  1516-1523   _is_process_running
  6859-6870   _is_quiet_hours
  1160-1169   _is_upload_window
 10321-10334  _json_error_handler
  7076-7106   _kick_broadcaster_id
 12646-12665  _kick_channel_live
  6993-7035   _kick_follower_count
 13657-13670  _kick_oauth_exchange
 13673-13675  _kick_oauth_page
 13616-13620  _kick_redirect_public
 13607-13613  _kick_redirect_source
 13593-13604  _kick_redirect_uri
  6978-6980   _kick_slug
 13623-13654  _kick_user_token
  3939-3942   _kind_from_filename
 15986-15991  _latest_popularity
 20259-20265  _learned_load
 20256-20257  _learned_path
 20267-20275  _learned_save
 22769-22799  _live_react_loop
 22565-22758  _live_react_worker
 21355-21366  _live_transcript_push
 22760-22767  _live_users
 21790-21834  _living_title_loop
 20216-20224  _load_banned_words_file
  1691-1764   _load_cookies_dict
 28598-28670  _local_backup_scan
 10303-10317  _log_5xx
 18728-18740  _looks_like_codec_err
 18723-18725  _looks_like_source_expired
  8110-8140   _loop_fehler
 15350-15359  _loop_heartbeat
 31222-31249  _loop_lag_monitor
 15469-15472  _loop_not_ready
 15362-15430  _loop_watchdog_thread
 21235-21249  _loyalty_add
 21226-21232  _loyalty_get
 21252-21260  _loyalty_top
 16370-16388  _manual_donations_rows
 16391-16393  _manual_donations_total
  8202-8203   _mark_dead
 12813-12842  _marketing_cfg
 12804-12810  _marketing_default_targets
 12799-12801  _marketing_enabled
 12856-12871  _marketing_flavor
 12926-12942  _marketing_loop
 12874-12884  _marketing_post_discord
 12887-12899  _marketing_post_telegram
 12902-12923  _marketing_publish
 12845-12849  _marketing_state_obj
 12852-12853  _marketing_state_save
 29929-29947  _maybe_handle_command
 31559-31583  _maybe_hype_clip
  3857-3880   _migrate_columns
 30206-30217  _mod_is_exempt
 30220-30225  _mod_warn_first
 30228-30231  _mod_warn_text
 17631-17639  _modlog
   913-915    _multistream_targets
  8041-8042   _nc_create_subprocess_exec
  8045-8046   _nc_create_subprocess_shell
 13037-13053  _news_cfg
 13024-13026  _news_enabled
 13091-13132  _news_facts
 13246-13268  _news_generate
 13451-13468  _news_loop
 13029-13034  _news_output_path
 13135-13137  _news_phrase
 13222-13243  _news_phrase_impl
 13066-13073  _news_read
 13056-13059  _news_state_obj
 13062-13063  _news_state_save
 13076-13088  _news_write
 17669-17671  _normalize_ingest
  2324-2341   _note_check_duration
 21381-21389  _oracle_memories
 21647-21681  _oracle_memorize
 21392-21405  _oracle_persona
 21374-21378  _oracle_recent_text
 17968-17976  _ov_atomic_write
 17956-17962  _ov_bar
 20172-20184  _ov_clip_text
 17965-17966  _ov_oneline
 24802-24831  _overlay_push
 18259-18302  _overlay_render_size
 17730-17734  _overlay_session_reset
 24750-24753  _overlay_src_ok
 20335-20345  _own_invites
 16351-16367  _parse_eur
 18254-18256  _parse_size
 26010-26090  _parse_ssh_attacks
  7465-7498   _pause_resume_cmd
  1819-1863   _persist_refreshed_cookies
  1657-1689   _pick_checked_pull_proxy
 10398-10411  _pin_auth_value
 10457-10458  _pin_clear_fail
 10437-10440  _pin_locked
 10443-10454  _pin_note_fail
 10414-10434  _pin_ok
 24640-24642  _piper_available
 24605-24627  _piper_list_voices
 24647-24672  _piper_pick_model
 24684-24731  _piper_say
 24598-24602  _piper_voice_roots
 15886-15921  _post_json_threaded
 18233-18251  _probe_video_size
  1544-1561   _proc_is_recorder
 11978-11989  _proxy_geo_cache_put
 12205-12231  _proxy_pool_refresh_loop
  1623-1654   _proxy_report_recording
 15315-15317  _prune_stall_dumps
 13271-13392  _public_stats
 21909-21935  _push_notify
 10559-10561  _pwa_dir
 11949-11964  _quick_validate_proxy
 15952-15954  _quiet_hours_config
 10524-10557  _rate_guard
 21200-21206  _react_warn
  7949-7988   _reap_proc
  2364-2386   _record_check_outcome
   704-706    _redact_stream_urls
 12132-12202  _refresh_proxy_pool
 24630-24636  _resolve_piper_model
 14590-14605  _resolve_tracked_user
  2158-2248   _resolve_via_html
  2506-2660   _resolve_via_webcast_api_v2
  2723-2785   _resolve_via_ytdlp
 29548-29677  _resolve_youtube_ingest
 22838-22845  _restream_active_platforms
 17715-17726  _restream_active_sources
 22419-22518  _restream_chat_guardian
 17880-17952  _restream_chat_push
 17642-17654  _restream_enabled
 18321-18408  _restream_html_overlay_start
 18411-18424  _restream_html_overlay_stop
  1108-1110   _restream_layout_mode
 17680-17703  _restream_overlay_files
 22803-22835  _restream_platform_state
 22966-23001  _restream_resume_after_restart
 18472-18530  _restream_tts_enqueue_wav
 18195-18227  _restream_tts_feeder
 18192-18193  _restream_tts_fifo_path
 18427-18454  _restream_tts_start
 18456-18470  _restream_tts_stop
 22848-22963  _restream_verify_loop
 28563-28575  _retention_loop
 28522-28560  _retention_scan
  2468-2470   _room_is_abo
  6309-6426   _run_ai_call
 15453-15466  _run_async_from_flask
 25811-25814  _run_priv
 32229-32237  _run_selfcheck_and_exit
 28578-28589  _s3_client
  8205-8251   _safe_send
  4792-4808   _sample_net_throughput
 20226-20234  _save_banned_words_file
  2416-2443   _schedule_next_check
 28481-28519  _scheduler_loop
  3883-3887   _schema_pk
 15474-15479  _scraper_session
 30234-30273  _screen_full
 13983-14020  _sec_headers
  2137-2139   _select_stream_from_data_section
 32042-32226  _selfcheck
  1183-1187   _should_defer_upload
 28989-29024  _shrink_for_discord
 10564-10576  _sicheres_ziel
 31480-31497  _sign_health_check
 31500-31519  _sign_health_loop
  8058-8069   _spawn
  8072-8102   _spawn_from_flask
 26134-26137  _st_befund
 22144-22385  _start_chat_listener
 15433-15450  _start_loop_watchdog
 13416-13442  _stats_loop
 13395-13398  _stats_output_path
 13401-13413  _stats_write
  8697-8711   _storage_cleanup_loop
 31539-31546  _story_for
  3175-3181   _stream_url_expiry
  3190-3196   _stream_url_is_fresh
  3183-3188   _stream_url_ttl
 20299-20306  _streamer_persona_get
 20281-20287  _streamer_personas_load
 20278-20279  _streamer_personas_path
 20289-20297  _streamer_personas_save
 18147-18151  _studio_chain
 28695-28817  _system_backup
 28820-28848  _system_backup_loop
 11901-11940  _test_proxy
 12687-12696  _testpush_cfg
 12699-12716  _testpush_exec
 12668-12684  _testpush_resolve_live
  8874-8884   _tg_topics_load_into_mem
  8871-8872   _tg_topics_path
  8886-8893   _tg_topics_save
 25344-25392  _tiktok_account_exists
 10372-10380  _token_ok
  8896-8900   _topic_forget
 15972-15983  _tracking_max_duration
  1410-1433   _try_attach_file_handler
 24674-24682  _tts_cleanup
 12572-12575  _tunnel_effective
 24100-24153  _twitch_channel_status
 30276-30419  _twitch_chat_loop
 30090-30193  _twitch_eventsub_loop
 16796-16799  _twitch_oauth_page
  1206-1219   _upload_queue_add
  1230-1232   _upload_queue_count
  1189-1198   _upload_queue_load
  1179-1181   _upload_queue_path
  1221-1228   _upload_queue_remove
  1200-1204   _upload_queue_save
  1234-1272   _upload_window_loop
  7922-7929   _uptime_s
 17657-17666  _url_host
   684-701    _url_ohne_zugang
   768-772    _usage_record_claude
  8143-8187   _verbindung_verloren
  7038-7066   _viewer_sample_loop
  7108-7115   _viewer_stats
 10461-10464  _wants_html
  7932-7946   _warn_empty_env
 31295-31390  _watchdog_loop
 29831-29839  _wchat_thank_ok
 21978-22008  _whisper_get_model
  8019-8026   _whisper_native_section
 21187-21193  _whisper_pool
 22077-22106  _whisper_segments
 22010-22074  _whisper_transcribe
 17978-18140  _write_restream_overlay
 30447-30520  _youtube_api_chat_loop
 24156-24259  _youtube_api_status
 24262-24329  _youtube_channel_status
 30523-30680  _youtube_chat_loop
 29683-29696  _youtube_restream_autoconfig
 29699-29723  _youtube_restream_autoconfig_inner
 29789-29817  _youtube_send
 24434-24475  _youtube_set_channel
 29726-29760  _yt_access_token
 29763-29778  _yt_live_chat_id
 30440-30444  _yt_oauth_configured
 29784-29786  _yt_sendrate_cfg
 30422-30437  _yt_timeout
  2707-2708   _ytdlp_detect_available
  2710-2721   _ytdlp_note_result
 15320-15322  _zombie_child_count
  7799-7823   about
  4058-4062   add_ai_log_entry
  3975-3978   add_archive_entry
  4905-4920   add_archive_rule
  4487-4521   add_recording
  4148-4165   add_tracking
  4582-4599   add_tracking_tag
  6429-6462   ai
  3722-3761   ai_chat
  3795-3805   ai_history_append
  3807-3812   ai_history_clear
  3784-3793   ai_history_load
  3769-3782   ai_rate_limit_check
  6491-6499   aireset
 21518-21537  azrael_chat
 30685-30807  brain_cmd
  3199-3383   build_recording_cmd
  4168-4245   bulk_add_trackings
  7296-7355   bulkadd
  8714-8854   check_all_trackings
  4332-4344   claim_live_transition
 20375-21130  class KickModerator
 18743-20059  class RestreamManager
 12316-12358  classify_proxy_anonymity
  6537-6735   cleanup
  5500-5541   cleanup_old_recordings
  4478-4485   clear_recording
 29434-29499  clip_moment
  5053-5096   cluster_failures
  4736-4785   compute_storage_forecast
  7418-7462   cookies_cmd
  5342-5348   cookies_days_old
  4139-4145   count_trackings_for_chat
  4045-4056   decide_preferred_recorder
  3985-3988   delete_archive_entry
  4922-4930   delete_archive_rule
  5966-6113   diag
 30919-30980  einnahmen_cmd
  4730-4733   find_recordings_by_fingerprint
  4006-4022   finish_recording_attempt
  4277-4287   get_all_active_trackings
  4084-4087   get_all_checks
  4523-4526   get_all_recordings
  4624-4634   get_all_tags_with_counts
  4707-4710   get_annotations_for_recording
  3980-3983   get_archive_entry
  4700-4703   get_bookmarked_recordings
  1886-2003   get_cookie_health
  4573-4579   get_event_log
  4029-4043   get_last_recording_attempt
  2788-2893   get_live_status
  5256-5259   get_manual_recordings
  4715-4718   get_or_compute_inspect_sync
  5576-5620   get_outcome_breakdown
  4681-4689   get_priority_poll_interval
  4883-4892   get_profile_snapshots
  4064-4074   get_recent_ai_log
  4024-4027   get_recent_recording_attempts
  4528-4531   get_recording_by_id
  4693-4696   get_recording_note
  3517-3540   get_redis
  4115-4131   get_stats
  5467-5498   get_storage_stats
  4614-4622   get_tags_for_tracking
  5023-5037   get_tiktok_status_distribution
  4668-4679   get_tracking_priority
  4346-4355   get_tracking_state
  4273-4275   get_trackings_for_group
  5272-5275   get_trash_recordings
  9558-10200  handle_recording_finished
  3905-3930   init_db
  5390-5444   inspect_stream_url
 24797-24799  is_revenue_platform
  4895-4903   list_archive_rules
  5770-5808   live
  8254-8262   live_check_worker
  3592-3626   llm_chat
  3649-3677   llm_chat_sync
  3634-3646   llm_list_models
  4539-4565   log_event
  1478-1511   log_recording_failure
  7612-7661   logs_cmd
 31587-32032  main
  6465-6488   on_ai_media
  7738-7764   on_ai_reply
  7767-7796   on_azrael_mention
  7828-7858   on_callback
 21540-21644  oracle_handle
  7501-7504   pause_tracking
  5630-5635   profile_keyboard
  5351-5387   quick_restart_tracking
  7563-7609   quota
  8631-8694   reaper_loop
  5019-5021   record_tiktok_status
  6504-6534   recstatus
  3542-3550   redis_get_json
  3552-3558   redis_set_json
  4247-4271   remove_tracking
  4601-4612   remove_tracking_tag
 30983-30993  report_cmd
 12361-12363  report_proxy_result
  2251-2278   resolve_tiktok_live_stream
  5267-5270   restore_recording
  7507-7510   resume_tracking
  4933-5013   run_archive_rules
 30996-31202  run_bot
 15242-15289  run_flask
  4811-4856   sample_bandwidth_for_active
  4862-4881   save_profile_snapshot
  4076-4082   save_tiktok_check
  4470-4476   set_recording_file
  4290-4328   set_tracking_paused
  4637-4666   set_tracking_priority
  5262-5265   soft_delete_recording
  8943-9556   split_and_send_video
  5683-5725   start
  3990-4004   start_recording_attempt
  6738-6776   stats
  5237-5254   stop_manual_recording
  7513-7560   stoprec
  6963-6971   summary_cmd
  7664-7735   sysres
  6115-6259   teststream
  5727-5768   tiktok
  7358-7415   topusers
  5845-5902   track
  5810-5842   track_exact
  5916-5964   tracklist
  5103-5235   trigger_manual_recording
  4431-4468   try_acquire_recording_lock
  5278-5337   universal_search
  5904-5914   untrack
 30810-30916  update_cmd
  4725-4728   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
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
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
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
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
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
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
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
